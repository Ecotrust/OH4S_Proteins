from django.db import models
from django.conf import settings

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.images.edit_handlers import ImageChooserPanel

from providers.views import header as get_header_context, get_category_context, get_homepage_filter_context, get_results_filter_context

class HomePage(Page):
    welcome = RichTextField(blank=True, verbose_name='Welcome Title')
    welcome_text = RichTextField(blank=True, default='<p>We connect school food buyers with Oregon producers who are ready to sell to schools. We have over 75 producers offering a wide variety of products. You can  search by product type, producer identity, location, and much more.</p><p>Need help using the site? <a href="https://vimeo.com/352842407" target="_blank">Watch our short how-to video</a> or <a href="/contact">contact us here</a>. Know a food producer who should be here? Thanks for visiting.</p>')
    filter_prompt = RichTextField(blank=True, help_text='Language directing users to use filters', default='Explore our filters')
    categories_header = RichTextField(blank=True, help_text='Header above categories', default='View  all  suppliers  for  specific  product  categories')
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('welcome', classname="full"),
        FieldPanel('welcome_text', classname="full"),
        FieldPanel('filter_prompt', classname="full"),
        FieldPanel('categories_header', classname="full"),
        ImageChooserPanel('image'),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        context = get_header_context(request, context)
        context = get_category_context(request, context)
        context = get_homepage_filter_context(request, context)
        if self.image == None:
            context['image'] = settings.DEFAULT_PROJECT_IMAGE
        else:
            context['image'] = self.image.file.url
        return context

class ResultsPage(Page):
    results_count_message = RichTextField(blank=True, default='Producers found:')
    filter_prompt = RichTextField(blank=True, help_text='Language directing users to use filters', default='You can filter these results further')

    content_panels = Page.content_panels + [
        FieldPanel('results_count_message', classname="full"),
        FieldPanel('filter_prompt', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context = get_header_context(request, context)
        context = get_results_filter_context(request, context)
        return context

class ContentPage(Page):
    content_title = RichTextField(blank=True, default='Page Title')
    content = RichTextField(blank=True, default='Page content...')

    content_panels = Page.content_panels + [
        FieldPanel('content_title', classname="full"),
        FieldPanel('content', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context = get_header_context(request, context)
        return context
