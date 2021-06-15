from django.shortcuts import render

# Create your views here.
def get_footer_context(request, context):
    from cms.models import FooterPage
    footer = FooterPage.objects.all()[0]
    footer_context = footer.get_context(request)
    for key in footer_context.keys():
        if not key == 'page':
            context[key] = footer_context[key]
        else:
            context['footer_page'] = footer_context['page']
    return context
