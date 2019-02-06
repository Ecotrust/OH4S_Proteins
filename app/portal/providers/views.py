from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def header(request, context, project_id=None):
    from providers.models import Project

    project = None
    project_context = {}
    if Project.objects.all().count() > 0:
        # There should never be more or less than one project, but...
        if project_id:
            try:
                project = Project.objects.get(pk=project_id)
            except Exception as e:
                pass
        if not project:
            project = Project.objects.all()[0]
        project_context['title'] = project.title
        project_context['welcome'] = project.welcome
        project_context['image'] = project.image
    else:
        project_context['title'] = settings.DEFAULT_PROJECT_TITLE
        project_context['welcome'] = settings.DEFAULT_PROJECT_WELCOME
        project_context['image'] = settings.DEFAULT_PROJECT_IMAGE

    context['PROJECT_TITLE'] = project_context['title']
    context['PROJECT_WELCOME'] = project_context['welcome']
    context['PROJECT_IMAGE'] = project_context['image']

    return context

def index(request):
    from providers.models import ProductCategory

    top_tier_categories = ProductCategory.objects.filter(parent=None)

    context = {
        'categories': [x.to_dict() for x in top_tier_categories.order_by('name')],
    }

    context = header(request, context)

    return render(request, "index.html", context)

def category(request, category_id):
    from providers.models import ProductCategory
    from providers.forms import FilterForm

    try:
        category = ProductCategory.objects.get(pk=category_id)
    except Exception as e:
        return index(request)
    children = [x.to_dict() for x in category.get_children().order_by('name')]
    provider_products = category.get_provider_products()
    product_details = [ (y, y) for y in [x['name'] for x in children ] ]
    production_capacity_unit = category.capacityMeasurement.unit
    filter_form = FilterForm(product_details=product_details, production_capacity_unit=production_capacity_unit)
    context = {
        'category': category.to_dict(),
        'children':  children,
        'provider_products': provider_products.order_by('name'),
        'filter_form': filter_form,
    }
    context = header(request, context)
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
    context = header(request, context)
    return render(request, "product.html", context)
