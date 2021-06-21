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

def get_header_context(request, context):
    from cms.models import Header
    headers = Header.objects.all()
    if headers.count() == 0:
        title = 'Oregon Harvest for Schools Directory'
        image = 'providers/img/defaults/logo-oh4s-large.jpg'
    else:
        title = headers[0].title
        image = headers[0].image

    context['header_title'] = title
    context['header_image'] = image
    return context
