from django.db import models
from django.conf import settings

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock, URLBlock, RawHTMLBlock, StructBlock, CharBlock, PageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet

from providers.views import get_category_context, get_homepage_filter_context, get_results_filter_context
from providers.models import Provider
from cms.views import get_header_context, get_footer_context

class LinkBlock(StructBlock):
    text = CharBlock()
    link = URLBlock()

class InternalLinkBlock(StructBlock):
    text = CharBlock()
    link = PageChooserBlock()

class PortalPage(Page):

    class Meta:
        abstract = True

    def get_context(self, request):
        context = super().get_context(request)
        context = get_header_context(request, context)
        context = get_footer_context(request, context)
        return context

class HomePage(PortalPage):
    welcome = models.CharField(max_length=255, default='Welcome', verbose_name='Welcome Title')
    welcome_text = RichTextField(
        blank=True,
        features=[
            'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr',
            'superscript', 'subscript', 'strikethrough', 'blockquote', 'image',
            'embed'
        ],
        default='<p><b>We connect school food buyers with Oregon producers who ' +
            'are ready to sell to schools</b></p>' +
            '<p><b>Get started by searching with out new filters or by ' +
            'selecting the product types pictured below.</b></p>' +
            '><p>Need help using the site? ' +
            '<a href="https://vimeo.com/352842407" target="_blank">' +
            'Watch our short how-to video</a>. Have ideas about how this site' +
            'cab be improved? <a hre="http://localhost:8000/contact" ' +
            'target="_blank">We want to her from you</a>.'
            '¿Habla Español? <a hre="http://localhost:8000/contact" ' +
            'target="_blank">Contáctanos aquí</a>.' +
            '</p>',
        verbose_name='Welcome Text'
    )
    filter_prompt = models.CharField(max_length=255, help_text='Language directing users to use filters', default='Search By Filtering')
    categories_header = models.CharField(max_length=255, help_text='Header above categories', default='Search By Product Types')

    content_panels = Page.content_panels + [
        FieldPanel('welcome', classname="full"),
        FieldPanel('welcome_text', classname="full"),
        FieldPanel('filter_prompt', classname="full"),
        FieldPanel('categories_header', classname="full"),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        context = get_category_context(request, context)
        context = get_homepage_filter_context(request, context)
        return context

class ResultsPage(PortalPage):
    subtitle = models.CharField(max_length=255, default='Results', help_text="Page header subtitle")
    results_count_message_before = models.CharField(max_length=255, blank=True, default='We found', help_text="Text before result count")
    results_count_message_after = models.CharField(max_length=255, blank=True, default='producers that meet your criteria', help_text="Text after result count")
    filter_advice = RichTextField(
    blank=True,
    features=[
    'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr',
    'superscript', 'subscript', 'strikethrough', 'blockquote', 'image',
    'embed'
    ],
    default='<p>Try removing filters to see more results</p>',
    help_text='Helpful advice for users confused by their results'
    )
    filter_prompt = models.CharField(max_length=255, help_text='Language directing users to use filters', default='Add Filters')

    content_panels = Page.content_panels + [
        FieldPanel('results_count_message_before', classname="full"),
        FieldPanel('results_count_message_after', classname="full"),
        FieldPanel('filter_advice', classname="full"),
        FieldPanel('filter_prompt', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context = get_results_filter_context(request, context)
        return context

class ProducerPage(RoutablePageMixin, PortalPage):
    subtitle = models.CharField(max_length=255, default='Producer Profile', help_text="Page header subtitle")
    bottom_blurb = StreamField([
        ('image', ImageChooserBlock()),
        ('text', RichTextBlock(blank=True,features=[
            'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr',
            'superscript', 'subscript', 'strikethrough', 'blockquote', 'image',
            'embed'
        ])),
        ('google_form', LinkBlock(label="Google Form Link", template="cms/google_form.html", help_text="The URL for the Google form. This will be loaded into a popup when clicked.")),
        ('HTML', RawHTMLBlock(label="Custom HTML", help_text="For fine-tuning very specific/custom blocks.")),
        ('Embedded_Media', EmbedBlock(label="Embedded Media"))
    ], min_num=0, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="full"),
        FieldPanel('bottom_blurb', classname="full"),
    ]

    @route(r'^$') # will override the default Page serving mechanism
    @route(r'^(\d+)/$')
    def producer(self, request, id=None):
        """
        View function for the producer page
        """
        if id:
            try:
                provider = Provider.objects.get(pk=id)
            except Exception as e:
                pass
        if not id:
            provider = Provider.objects.all()[0]

        # NOTE: We can use the RoutablePageMixin.render() method to render
        # the page as normal, but with some of the context values overridden
        return self.render(request, context_overrides={
            'provider': provider,
        })

    def get_context(self, request):
        context = super().get_context(request)
        return context

class ContentPage(PortalPage):
    content_title = RichTextField(blank=True, default='Page Title')
    content = StreamField([
        ('image', ImageChooserBlock()),
        ('text', RichTextBlock(blank=True,features=[
            'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr',
            'superscript', 'subscript', 'strikethrough', 'blockquote', 'image',
            'embed'
        ])),
        ('google_form', LinkBlock(label="Google Form Link", template="cms/google_form.html", help_text="The URL for the Google form. This will be loaded into a popup when clicked.")),
        ('HTML', RawHTMLBlock(label="Custom HTML", help_text="For fine-tuning very specific/custom blocks.")),
        ('Embedded_Media', EmbedBlock(label="Embedded Media"))
    ])

    content_panels = Page.content_panels + [
        FieldPanel('content_title', classname="full"),
        FieldPanel('content', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        return context

class FooterPage(Page):
    footer_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    column_1 = StreamField([
        ('image', ImageChooserBlock()),
        ('externalLink', LinkBlock(label="External Link", template="cms/external_link.html")),
        ('internalLink', InternalLinkBlock(label="Internal Link", template="cms/internal_link.html")),
        ('google_form', LinkBlock(label="Google Form Link", template="cms/google_form_footer.html", help_text="The URL for the Google form. This will be loaded into a popup when clicked.")),
        ('text', RichTextBlock(features=[
            'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr',
            'superscript', 'subscript', 'strikethrough', 'blockquote', 'image',
            'embed'
        ])),
    ])
    column_2 = StreamField([
        ('image', ImageChooserBlock()),
        ('externalLink', LinkBlock(label="External Link", template="cms/external_link.html")),
        ('internalLink', InternalLinkBlock(label="Internal Link", template="cms/internal_link.html")),
        ('google_form', LinkBlock(label="Google Form Link", template="cms/google_form_footer.html", help_text="The URL for the Google form. This will be loaded into a popup when clicked.")),
        ('text', RichTextBlock(features=[
            'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr',
            'superscript', 'subscript', 'strikethrough', 'blockquote', 'image',
            'embed'
        ])),
    ])
    column_3 = StreamField([
        ('image', ImageChooserBlock()),
        ('externalLink', LinkBlock(label="External Link", template="cms/external_link.html")),
        ('internalLink', InternalLinkBlock(label="Internal Link", template="cms/internal_link.html")),
        ('google_form', LinkBlock(label="Google Form Link", template="cms/google_form_footer.html", help_text="The URL for the Google form. This will be loaded into a popup when clicked.")),
        ('text', RichTextBlock(features=[
            'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr',
            'superscript', 'subscript', 'strikethrough', 'blockquote', 'image',
            'embed'
        ])),
    ])

    content_panels = Page.content_panels + [
        ImageChooserPanel('footer_image'),
        StreamFieldPanel('column_1'),
        StreamFieldPanel('column_2'),
        StreamFieldPanel('column_3'),
    ]

@register_snippet
class Header(models.Model):
    title = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('image')
    ]

    def __str__(self):
        return self.title

@register_snippet
class Filter(models.Model):
    FACET_CHOICES = (
        (None, '----------'),
        ('identities', 'Self Identity'),
        ('availability', 'Availability by County'),
        ('component_categories', 'USDA Meal Component'),
        ('physical_counties', 'Producer Location: County'),
        ('delivery_methods', 'Delivery Methods'),
        ('product_categories', 'Product Categories'),
        ('product_forms', 'Product details'),
    )
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True, default=None)
    facet = models.CharField(
        max_length=255,
        choices = FACET_CHOICES,
        unique = True,
        default = None,
        blank = True
    )
    blurb = RichTextField(blank=True, default='You can select multiple options to include more producers.')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    order = models.IntegerField(default=10)

    def __str__(self):
        return "{} - {}: {}".format(self.order, self.name, self.facet)
