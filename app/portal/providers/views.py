from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from providers.models import ProductCategory, Project, Provider, ProviderProduct, Identity, PoliticalSubregion, ComponentCategory, DeliveryMethod, Distributor, ProductionPractice
from providers.forms import FilterForm
import json

def header(request, context, project_id=None):
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

def get_category_context(request, context):

    top_tier_categories = ProductCategory.objects.filter(parent=None)

    context['categories'] = [x.to_dict() for x in top_tier_categories.order_by('name')]
    context['default_image'] = settings.DEFAULT_CATEGORY_IMAGE

    return context

def index(request):
    context = header(request, context)
    context = get_category_context(request, context)

    return render(request, "index.html", context)

def get_homepage_filter_context(request, context={}):
    # TODO: Build and return Homepage Filter Context
    return context

def get_results_filter_context(request, context={}):
    # TODO: Based on current applied filters in request.body
    # add 'filters' to context and build it with current filter state
    return context

def category(request, category_id):
    try:
        category = ProductCategory.objects.get(pk=category_id)
    except Exception as e:
        return index(request)
    children = category.get_children()
    providers = category.get_providers()
    product_details = [ (x.pk, x.name) for x in children ]
    if category.capacityMeasurement:
        production_capacity_unit = category.capacityMeasurement.unit
    else:
        production_capacity_unit = settings.DEFAULT_CAPACITY_UNIT
    filter_form = FilterForm(product_details=product_details, production_capacity_unit=production_capacity_unit)
    context = {
        'category': category.to_dict(),
        # 'children':  [x.to_dict() for x in children.order_by('name')],
        'providers': providers.order_by('name'),
        'filter_form': filter_form,
    }
    context = header(request, context)

    return render(request, "category.html", context)

def all_categories(request):
    children = ProductCategory.objects.filter(parent=None)
    providers = Provider.objects.all()
    product_details = [ (x.pk, x.name) for x in children ]
    # TODO - hide production capacity filter field
    production_capacity_unit = settings.DEFAULT_CAPACITY_UNIT
    filter_form = FilterForm(product_details=product_details, production_capacity_unit=production_capacity_unit)
    context = {
        'category': {
            'pk': None,
            'image': settings.DEFAULT_CATEGORY_IMAGE,
            'name': "All",
        },
        'providers': providers.order_by('name'),
        'filter_form': filter_form,
    }
    context = header(request, context)

    return render(request, "category.html", context)

def filterByCategory(request, category_id=None):
    if category_id:
        category = ProductCategory.objects.get(pk=category_id)
        provider_products = category.get_provider_products()
    else:
        category = None
        provider_products = ProviderProduct.objects.all()

    if request.method == "POST":
        if 'product_category' in request.POST.keys():
            product_ids = []
            for category_id in request.POST.getlist('product_category'):
                filter_category = ProductCategory.objects.get(pk=int(category_id))
                product_ids += [x.pk for x in filter_category.get_provider_products()]
            provider_products = provider_products.filter(pk__in=product_ids)

        try:
            if category and 'capacity' in request.POST.keys() and not request.POST.get('capacity') == '' and not int(request.POST.get('capacity')) == 0:
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

    return provider_products

def filterProducts(request, category_id=None):
    provider_products = filterByCategory(request, category_id)

    context = {
        'provider_products': provider_products.order_by('name'),
    }
    return render(request, "product_results.html", context)

def filterProviders(request, category_id=None):
    provider_products = filterByCategory(request, category_id)
    provider_ids = [x.provider.pk for x in provider_products]
    providers = Provider.objects.filter(pk__in=provider_ids)

    context = {
        'providers': providers.order_by('name'),
    }
    return render(request, "provider_results.html", context)

def product(request, product_id):
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
    try:
        provider = Provider.objects.get(pk=provider_id)
        products = ProviderProduct.objects.filter(provider=provider)
    except Exception as e:
        return index(request)
    context = {
        'provider': provider.to_dict(),
        'products': [x.to_dict() for x in products.order_by('name')],
    }
    context = header(request, context)
    return render(request, "provider.html", context)

#   A generic results page. This should load blank, then make an ajax request
# to the following 'filter' view to populate the template with filter results.
# Further changes to the filters on the page should trigger additional ajax
# requests to update the data. There should be no page refreshes.
def results(request):
    context = {
        'category': {
            'pk': None,
            'image': settings.DEFAULT_CATEGORY_IMAGE,
            'name': "All",
        },
        'providers': [],
        # 'filter_form': None,
    }
    context = header(request, context)

    return render(request, "category.html", context)

#   requests should have a 'filters' object that gets parsed, run against the
# providers records, then an alphabetical list of results should be put into
# the JsonResponse and sent back to the client to render.
def filter(request):
    providers = Provider.objects.all()
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except Exception as e:
            print(e)
            body = {}
        if 'product_categories' in body.keys():
            # Many-to-many (OR)
            product_ids = []
            for filter_category in ProductCategory.objects.filter(pk__in=body['product_categories']):
                product_ids += [x.pk for x in filter_category.get_provider_products()]
            provider_products = ProviderProduct.objects.filter(pk__in=product_ids)
            provider_ids = [x.provider.pk for x in provider_products]
            providers = providers.filter(pk__in=provider_ids)
        if 'identities' in body.keys():
            # Many-to-many (OR)
            identities = Identity.objects.filter(pk__in=body['identities'])
            provider_ids = []
            for identity in identities:
                new_provider_ids = [x.pk for x in identity.provider_set.all()]
                provider_ids = list(set(provider_ids + new_provider_ids))
            providers = providers.filter(pk__in=provider_ids)
        if 'availability' in body.keys():
            # Many-to-many (OR)
            regions = PoliticalSubregion.objects.filter(pk__in=body['availability'])
            provider_ids = []
            for region in regions:
                new_provider_ids = [x.pk for x in region.provider_set.all()]
                provider_ids = list(set(provider_ids + new_provider_ids))
            providers = providers.filter(pk__in=provider_ids)
        if 'physical_counties' in body.keys():
            # Many-to-many (OR)
            regions = PoliticalSubregion.objects.filter(pk__in=body['physical_counties'])
            provider_ids = []
            for region in regions:
                new_provider_ids = [x.pk for x in providers.filter(physicalCounty=region)]
                provider_ids = list(set(provider_ids + new_provider_ids))
            providers = providers.filter(pk__in=provider_ids)

        if 'component_categories' in body.keys():
            # Many-to-many (OR)
            components = ComponentCategory.objects.filter(pk__in=body['component_categories'])
            provider_ids = []
            for component in components:
                for provider in providers:
                    if component in provider.components_offered and not provider.id in provider_ids:
                        provider_ids.append(provider.id)
            providers = providers.filter(pk__in=provider_ids)
        if 'delivery_methods' in body.keys():
            # Many-to-many (OR)
            delivery_methods = DeliveryMethod.objects.filter(pk__in=body['delivery_methods'])
            provider_ids = []
            for method in delivery_methods:
                new_provider_ids = [x.pk for x in method.provider_set.all()]
                provider_ids = list(set(provider_ids + new_provider_ids))
            providers = providers.filter(pk__in=provider_ids)
        if 'distributors' in body.keys():
            # Many-to-many (OR)
            distributors = Distributor.objects.filter(pk__in=body['distributors'])
            provider_ids = []
            for distributor in distributors:
                new_provider_ids = [x.pk for x in distributor.provider_set.all()]
                provider_ids = list(set(provider_ids + new_provider_ids))
            providers = providers.filter(pk__in=provider_ids)
        if 'practices' in body.keys():
            # Many-to-many (OR)
            practices = ProductionPractice.objects.filter(pk__in=body['practices'])
            provider_ids = []
            for practice in practices:
                new_provider_ids = [x.pk for x in practice.provider_set.all()]
                provider_ids = list(set(provider_ids + new_provider_ids))
            providers = providers.filter(pk__in=provider_ids)
        if 'product_forms' in body.keys():
            product_forms = ProductCategory.objects.filter(pk__in=body['product_forms'])
            provider_ids = []
            for form in product_forms:
                new_provider_ids = [x.pk for x in providers.filter(providerproduct__category=form)]
                provider_ids = list(set(provider_ids + new_provider_ids))
            providers = providers.filter(pk__in=provider_ids)

    providers_response = {'providers': []}
    for provider in providers:
      providers_response['providers'].append(provider.to_json())

    # TODO: determine correct filters that can be universally applied given current provider context
    filters_reponse = request.POST
    # TODO: apply provided filter state from request to this new filter list

    data = [providers_response, filters_reponse]
    return JsonResponse(data, safe=False)
