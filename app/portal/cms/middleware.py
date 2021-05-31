from django.middleware.csrf import CsrfViewMiddleware
from wagtail.core.views import serve

from cms.models import ResultsPage

# This code is here to support CSRF-Exempt calls to Wagtail Models' views
# As discussed here: https://github.com/wagtail/wagtail/issues/3066#issuecomment-609410019

class CustomWagtailCsrfViewMiddleware(CsrfViewMiddleware):

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if callback == serve:
            # We are visiting a wagtail page. Check if this is a ResultsPage
            # and if so, do not perfom any CSRF validation
            page = ResultsPage.objects.first()
            path = callback_args[0]

            if page and path.startswith(page.get_url_parts()[-1][1:]):
                return None

        return super().process_view(request, callback, callback_args, callback_kwargs)
