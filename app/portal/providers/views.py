from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    from providers.models import ProductCategory

    top_tier_categories = ProductCategory.objects.filter(parent=None)

    context = {
        'categories': [x.to_dict() for x in top_tier_categories],
    }

    return render(request, "index.html", context)

    # return HttpResponse("Hello, World. This is the providers index.")
