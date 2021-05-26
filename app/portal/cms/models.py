from django.db import models
from django.conf import settings

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.images.edit_handlers import ImageChooserPanel

from providers.views import header as get_header_context, get_category_context, get_homepage_filter_context

class HomePage(Page):
    welcome = RichTextField(blank=True)
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('welcome', classname="full"),
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
