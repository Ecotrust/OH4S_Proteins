from django.db import models
from django.conf import settings

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.images.edit_handlers import ImageChooserPanel

from providers.views import header as get_header_context, get_category_context, get_homepage_filter_context, get_results_filter_context

class HomePage(Page):
    welcome = models.CharField(max_length=255, default='Welcome', verbose_name='Welcome Title')
    welcome_text = RichTextField(
        blank=True,
        features=[
            'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr',
            'superscript', 'subscript', 'strikethrough', 'blockquote', 'image',
            'embed', 'code'
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
        context = get_header_context(request, context)
        context = get_category_context(request, context)
        context = get_homepage_filter_context(request, context)
        return context

class ResultsPage(Page):
    subtitle = models.CharField(max_length=255, default='Results', help_text="Page header subtitle")
    results_count_message_before = models.CharField(max_length=255, blank=True, default='We found', help_text="Text before result count")
    results_count_message_after = models.CharField(max_length=255, blank=True, default='producers that meet your criteria', help_text="Text after result count")
    filter_advice = RichTextField(
    blank=True,
    features=[
    'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr',
    'superscript', 'subscript', 'strikethrough', 'blockquote', 'image',
    'embed', 'code'
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
