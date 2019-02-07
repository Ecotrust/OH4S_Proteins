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
    children = category.get_children()
    provider_products = category.get_provider_products()
    product_details = [ (x.pk, x.name) for x in children ]
    if category.capacityMeasurement:
        production_capacity_unit = category.capacityMeasurement.unit
    else:
        production_capacity_unit = settings.DEFAULT_CAPACITY_UNIT
    filter_form = FilterForm(product_details=product_details, production_capacity_unit=production_capacity_unit)
    context = {
        'category': category.to_dict(),
        'children':  [x.to_dict() for x in children.order_by('name')],
        'provider_products': provider_products.order_by('name'),
        'filter_form': filter_form,
    }
    context = header(request, context)

    return render(request, "category.html", context)

def filterProducts(request, category_id):
    from providers.models import ProductCategory

    category = ProductCategory.objects.get(pk=category_id)
    provider_products = category.get_provider_products()

    if request.method == "POST":
        if 'product_category' in request.POST.keys():
            product_ids = []
            for category_id in request.POST.getlist('product_category'):
                filter_category = ProductCategory.objects.get(pk=int(category_id))
                product_ids += [x.pk for x in filter_category.get_provider_products()]
            provider_products = provider_products.filter(pk__in=product_ids)

        try:
            if 'capacity' in request.POST.keys() and not request.POST.get('capacity') == '' and not int(request.POST.get('capacity')) == 0:
                if category.capacityMeasurement:
                    production_capacity_unit = category.capacityMeasurement.unit
                else:
                    production_capacity_unit = settings.DEFAULT_CAPACITY_UNIT
                provider_products = provider_products.filter(capacityValue__gte=int(request.POST.get('capacity')), capacityMeasurement__unit=production_capacity_unit)
        except Exception as e:
            # RDH: just in case value is non-numeric
            pass

        try:
            if 'distribution' in request.POST.keys() and not int(request.POST.get('distribution')) < 0:
                provider_products = provider_products.filter(provider__deliveryMethods__pk=int(request.POST.get('distribution')))
        except Exception as e:
            # RDH: just in case value is non-numeric
            pass

        try:
            if 'availability' in request.POST.keys() and not int(request.POST.get('availability')) < 0:
                provider_products = provider_products.filter(provider__regionalAvailability__pk=int(request.POST.get('availability')))
        except Exception as e:
            # RDH: just in case value is non-numeric
            pass

    context = {
        'provider_products': provider_products.order_by('name'),
    }
    return render(request, "product_results.html", context)

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

def provider(request, provider_id):
    from providers.models import Provider
    try:
        provider = Provider.objects.get(pk=provider_id)
    except Exception as e:
        return index(request)
    context = {
        'provider': provider.to_dict(),
    }
    context = header(request, context)
    return render(request, "provider.html", context)
