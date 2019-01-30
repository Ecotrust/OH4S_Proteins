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

def category(request, category_id):
    from providers.models import ProductCategory

    try:
        category = ProductCategory.objects.get(pk=category_id)
    except Exception as e:
        return index(request)
    children = category.get_children()
    provider_products = category.get_provider_products()
    context = {
        'category': category,
        'children': [x.to_dict() for x in children],
        'provider_products': provider_products,
    }
    return render(request, "category.html", context)

def product(request, product_id):
    from providers.models import ProviderProduct
    try:
        product = ProviderProduct.objects.get(pk=product_id)
    except Exception as e:
        return index(request)
    context = {
        'product': product.to_dict(),
    }
    return render(request, "product.html", context)
