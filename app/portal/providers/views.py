from django.db.models import Q, Case, When
from django.db.models.functions import Greatest
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.views.decorators.csrf import csrf_exempt
from providers.models import ProductCategory, Project, Provider, ProviderProduct, Identity, PoliticalSubregion, ComponentCategory, DeliveryMethod, Distributor, ProductionPractice, Language
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
    from cms.models import Filter
    # Build and return Homepage Filter Context
    filters = []
    cms_filters = Filter.objects.all()

    try:
        filter_obj = cms_filters.get(facet='identities')
        identity_filter = {
            'name': filter_obj.name,
            'title': filter_obj.title if filter_obj.title else filter_obj.name,
            'facet': filter_obj.facet,
            'image': filter_obj.image.file.url if filter_obj.image else None,
            'blurb': filter_obj.blurb,
            'order': filter_obj.order,
            'widget': 'multiselect',
            'options': []
        }
    except Exception as e:
        identity_filter = {
            'name': 'Producer Identity',
            'title': 'Producer Identity',
            'facet': 'identities',
            'image': '/static/providers/img/defaults/filter_header.png',
            'widget': 'multiselect',
            'blurb': 'You can select multiple options to get more inclusive results.',
            'order': 0,
            'options': []
        }

    for identity in Identity.objects.all().order_by('name'):
        identity_filter['options'].append({
            'value': identity.pk,
            'label': identity.name,
            'state': False
        })
    filters.append(identity_filter)

    try:
        filter_obj = cms_filters.get(facet='availability')
        availability_filter = {
            'name': filter_obj.name,
            'title': filter_obj.title if filter_obj.title else filter_obj.name,
            'facet': filter_obj.facet,
            'image': filter_obj.image.file.url if filter_obj.image else None,
            'blurb': filter_obj.blurb,
            'order': filter_obj.order,
            'widget': 'multiselect',
            'options': []
        }
    except Exception as e:
        availability_filter = {
            'name': 'Availability',
            'title': 'Availability',
            'facet': 'availability',
            'image': '/static/providers/img/defaults/filter_header.png',
            'widget': 'multiselect',
            'blurb': 'You can select multiple options to get more inclusive results.',
            'order': 1,
            'options': []
        }

    for county in PoliticalSubregion.objects.all().order_by('name'):
        availability_filter['options'].append({
            'value': county.pk,
            'label': county.name,
            'state': False
        })
    filters.append(availability_filter)

    try:
        filter_obj = cms_filters.get(facet='component_categories')
        component_filter = {
            'name': filter_obj.name,
            'title': filter_obj.title if filter_obj.title else filter_obj.name,
            'facet': filter_obj.facet,
            'image': filter_obj.image.file.url if filter_obj.image else None,
            'blurb': filter_obj.blurb,
            'order': filter_obj.order,
            'widget': 'multiselect',
            'options': []
        }
    except Exception as e:
        component_filter = {
            'name': 'USDA Meal Components',
            'title': 'USDA Meal Components',
            'facet': 'component_categories',
            'image': '/static/providers/img/defaults/filter_header.png',
            'widget': 'multiselect',
            'blurb': 'You can select multiple options to get more inclusive results.',
            'order': 2,
            'options': []
        }

    for category in ComponentCategory.objects.all().order_by('order', 'name'):
        component_filter['options'].append({
            'value': category.pk,
            'label': category.name,
            'state': False
        })
    filters.append(component_filter)

    # Re-Order filters by 'order'
    filters.sort(key=lambda x: x['order'])

    context['filters'] = filters
    return context

@csrf_exempt
def get_results_filter_context(request, context={}):
    from cms.models import Filter
    # Based on current applied filters in request.body
    # add 'filters' to context and build it with current filter state
    filters = []
    current_state = {}
    cms_filters = Filter.objects.all()

    if request.method == "POST":
        try:
            current_state = json.loads(request.body)
        except Exception as e:
            try:
                current_state = dict(request.POST)
            except Exception as e:
                print(e)
                current_state = {}

    try:
        filter_obj = cms_filters.get(facet='identities')
        identity_filter = {
            'name': filter_obj.name,
            'title': filter_obj.title if filter_obj.title else filter_obj.name,
            'facet': filter_obj.facet,
            'image': filter_obj.image.file.url if filter_obj.image else None,
            'blurb': filter_obj.blurb,
            'order': filter_obj.order,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    except Exception as e:
        identity_filter = {
            'name': 'Producer Identity',
            'title': 'Producer Identity',
            'facet': 'identities',
            'image': '/static/providers/img/defaults/filter_header.png',
            'blurb': 'You can select multiple options to get more inclusive results.',
            'visible': True,
            'widget': 'multiselect',
            'order': 0,
            'options': []
        }
    for identity in Identity.objects.all().order_by('name'):
        identity_filter['options'].append({
            'value': identity.pk,
            'label': identity.name,
            'state': 'identities' in current_state.keys() and identity.pk in [int(x) for x in current_state['identities']]
        })
    filters.append(identity_filter)

    try:
        filter_obj = cms_filters.get(facet='availability')
        availability_filter = {
            'name': filter_obj.name,
            'title': filter_obj.title if filter_obj.title else filter_obj.name,
            'facet': filter_obj.facet,
            'image': filter_obj.image.file.url if filter_obj.image else None,
            'blurb': filter_obj.blurb,
            'order': filter_obj.order,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    except Exception as e:
        availability_filter = {
            'name': 'Availability',
            'title': 'Availability',
            'facet': 'availability',
            'image': '/static/providers/img/defaults/filter_header.png',
            'blurb': 'You can select multiple options to get more inclusive results.',
            'order': 1,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    for county in PoliticalSubregion.objects.all().order_by('name'):
        availability_filter['options'].append({
            'value': county.pk,
            'label': county.name,
            'state': 'availability' in current_state.keys() and county.pk in [int(x) for x in current_state['availability']]
        })
    filters.append(availability_filter)

    try:
        filter_obj = cms_filters.get(facet='component_categories')
        component_filter = {
            'name': filter_obj.name,
            'title': filter_obj.title if filter_obj.title else filter_obj.name,
            'facet': filter_obj.facet,
            'image': filter_obj.image.file.url if filter_obj.image else None,
            'blurb': filter_obj.blurb,
            'order': filter_obj.order,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    except Exception as e:
        component_filter = {
            'name': 'USDA Meal Components',
            'title': 'USDA Meal Components',
            'facet': 'component_categories',
            'image': '/static/providers/img/defaults/filter_header.png',
            'blurb': 'You can select multiple options to get more inclusive results.',
            'order': 2,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    for category in ComponentCategory.objects.all().order_by('order', 'name'):
        component_filter['options'].append({
            'value': category.pk,
            'label': category.name,
            'state': 'component_categories' in current_state.keys() and category.pk in [int(x) for x in current_state['component_categories']]
        })
    filters.append(component_filter)


    try:
        filter_obj = cms_filters.get(facet='physical_counties')
        location_filter = {
            'name': filter_obj.name,
            'title': filter_obj.title if filter_obj.title else filter_obj.name,
            'facet': filter_obj.facet,
            'image': filter_obj.image.file.url if filter_obj.image else None,
            'blurb': filter_obj.blurb,
            'order': filter_obj.order,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    except Exception as e:
        location_filter = {
            'name': 'Producer Location',
            'title': 'Producer Location',
            'facet': 'physical_counties',
            'image': '/static/providers/img/defaults/filter_header.png',
            'blurb': 'You can select multiple options to get more inclusive results.',
            'order': 3,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    for county in PoliticalSubregion.objects.all().order_by('name'):
        location_filter['options'].append({
            'value': county.pk,
            'label': county.name,
            'state': 'physical_counties' in current_state.keys() and county.pk in [int(x) for x in current_state['physical_counties']]
        })
    filters.append(location_filter)

    try:
        filter_obj = cms_filters.get(facet='delivery_methods')
        delivery_filter = {
            'name': filter_obj.name,
            'title': filter_obj.title if filter_obj.title else filter_obj.name,
            'facet': filter_obj.facet,
            'image': filter_obj.image.file.url if filter_obj.image else None,
            'blurb': filter_obj.blurb,
            'order': filter_obj.order,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    except Exception as e:
        delivery_filter = {
            'name': 'Delivery Method',
            'title': 'Delivery Method',
            'facet': 'delivery_methods',
            'image': '/static/providers/img/defaults/filter_header.png',
            'blurb': 'You can select multiple options to get more inclusive results.',
            'order': 4,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    for method in DeliveryMethod.objects.all().order_by('name'):
        delivery_filter['options'].append({
            'value': method.pk,
            'label': method.name,
            'state': 'delivery_methods' in current_state.keys() and method.pk in [int(x) for x in current_state['delivery_methods']]
        })
    filters.append(delivery_filter)

    try:
        filter_obj = cms_filters.get(facet='product_categories')
        category_filter = {
            'name': filter_obj.name,
            'title': filter_obj.title if filter_obj.title else filter_obj.name,
            'facet': filter_obj.facet,
            'image': filter_obj.image.file.url if filter_obj.image else None,
            'blurb': filter_obj.blurb,
            'order': filter_obj.order,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    except Exception as e:
        category_filter = {
            'name': 'Product Type',
            'title': 'Product Type',
            'facet': 'product_categories',
            'image': '/static/providers/img/defaults/filter_header.png',
            'blurb': 'You can select multiple options to get more inclusive results.',
            'order': 5,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }

    for category in ProductCategory.objects.filter(parent=None).order_by('name'):
        category_filter['options'].append({
            'value': category.pk,
            'label': category.name,
            'state': 'product_categories' in current_state.keys() and category.pk in [int(x) for x in current_state['product_categories']]
        })
    filters.append(category_filter)

    try:
        filter_obj = cms_filters.get(facet='product_forms')
        details_filter = {
            'name': filter_obj.name,
            'title': filter_obj.title if filter_obj.title else filter_obj.name,
            'facet': filter_obj.facet,
            'image': filter_obj.image.file.url if filter_obj.image else None,
            'blurb': filter_obj.blurb,
            'order': filter_obj.order,
            'visible': True,
            'widget': 'compound-multiselect',
            'option_categories': [],
            'options': {}
        }
    except Exception as e:
        details_filter = {
            'name': 'Product Details',
            'title': 'Product Details',
            'facet': 'product_forms',
            'image': '/static/providers/img/defaults/filter_header.png',
            'blurb': 'You can select multiple options to get more inclusive results.',
            'order': 6,
            'visible': True,
            'widget': 'compound-multiselect',
            'option_categories': [],
            'options': {}
        }

    for category in ProductCategory.objects.exclude(parent=None).order_by('name'):
        prime_category = category.get_prime_ancestor()
        prime_name = prime_category.name
        if prime_name not in details_filter['options'].keys():
            details_filter['options'][prime_name] = []
            details_filter['option_categories'].append((prime_name, prime_category.id))

        if ' > ' in str(category):
            label = ' > '.join(str(category).split(' > ')[1:])
        else:
            label = str(category)
        details_filter['options'][prime_name].append({
            'value': category.pk,
            'label': label,
            'state': 'product_forms' in current_state.keys() and category.pk in [int(x) for x in current_state['product_forms']]
        })
        details_filter['options'][prime_name] = sorted(details_filter['options'][prime_name], key = lambda i: (i['label'].lower()))
    details_filter['option_categories'].sort()
    filters.append(details_filter)

    try:
        filter_obj = cms_filters.get(facet='distributors')
        distributor_filter = {
            'name': filter_obj.name,
            'title': filter_obj.title if filter_obj.title else filter_obj.name,
            'facet': filter_obj.facet,
            'image': filter_obj.image.file.url if filter_obj.image else None,
            'blurb': filter_obj.blurb,
            'order': filter_obj.order,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    except Exception as e:
        distributor_filter = {
            'name': 'Distributors',
            'title': 'Distributors',
            'facet': 'distributors',
            'image': '/static/providers/img/defaults/filter_header.png',
            'blurb': 'You can select multiple options to get more inclusive results.',
            'order': 7,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    for distributor in Distributor.objects.all().order_by('name'):
        distributor_filter['options'].append({
            'value': distributor.pk,
            'label': distributor.name,
            'state': 'distributors' in current_state.keys() and distributor.pk in [int(x) for x in current_state['distributors']]
        })
    filters.append(distributor_filter)

    try:
        filter_obj = cms_filters.get(facet='practices')
        practice_filter = {
            'name': filter_obj.name,
            'title': filter_obj.title if filter_obj.title else filter_obj.name,
            'facet': filter_obj.facet,
            'image': filter_obj.image.file.url if filter_obj.image else None,
            'blurb': filter_obj.blurb,
            'order': filter_obj.order,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    except Exception as e:
        practice_filter = {
            'name': 'Production Practices',
            'title': 'Production Practices',
            'facet': 'practices',
            'image': '/static/providers/img/defaults/filter_header.png',
            'blurb': 'You can select multiple options to get more inclusive results.',
            'order': 8,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    for practice in ProductionPractice.objects.all().order_by('name'):
        practice_filter['options'].append({
            'value': practice.pk,
            'label': practice.name,
            'state': 'practices' in current_state.keys() and practice.pk in [int(x) for x in current_state['practices']]
        })
    filters.append(practice_filter)

    try:
        filter_obj = cms_filters.get(facet='languages')
        language_filter = {
            'name': filter_obj.name,
            'title': filter_obj.title if filter_obj.title else filter_obj.name,
            'facet': filter_obj.facet,
            'image': filter_obj.image.file.url if filter_obj.image else None,
            'blurb': filter_obj.blurb,
            'order': filter_obj.order,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    except Exception as e:
        language_filter = {
            'name': 'Language Spoken',
            'title': 'Language Spoken',
            'facet': 'languages',
            'image': '/static/providers/img/defaults/filter_header.png',
            'blurb': 'You can select multiple options to get more inclusive results.',
            'order': 9,
            'visible': True,
            'widget': 'multiselect',
            'options': []
        }
    for language in Language.objects.all().order_by('name'):
        language_filter['options'].append({
            'value': language.pk,
            'label': language.name,
            'state': 'languages' in current_state.keys() and language.pk in [int(x) for x in current_state['languages']]
        })

    filters.append(language_filter)

    # Re-Order filters by 'order'
    filters.sort(key=lambda x: x['order'])

    # Add search keywords if any
    try:
        filters.append({'keywords': current_state['keywords'][0]})
    except Exception as e:
        filters.append({'keywords': ''})

    context['filters'] = filters
    context['filters_json'] = json.dumps(filters)
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

def run_keyword_search(queryset, model, keyword, fields, fk_fields, weight_lookup, sort_field):
    # queryset -> a pre-filtered list of objects to select from
    # model -> the model calling this function
    # keyword -> [str] your search string -- can be multiple words
    # fields -> [list of str] char or text fields on your model
    # fk_fields -> [list of tuples] Foreign Key field names coupled with field on foreign model to search
    #   fk_fields can search any models with a fk for current model as well!
    # weight_lookup -> [dict] lookup to get relative ['A','B','C','D'] weights for scoring search results.

    if keyword == '':
        return queryset
        
    similarities = []
    vector = False
    similarity = False
    for idx, val in enumerate(fields):
        similarities.append(TrigramSimilarity(val, keyword, weight=weight_lookup[val]))
        if idx == 0:
            vector = SearchVector(val, weight=weight_lookup[val])
        else:
            vector += SearchVector(val, weight=weight_lookup[val])

    for val in fk_fields:
        relationship_name = '__'.join(val)
        similarities.append(TrigramSimilarity(relationship_name, keyword, weight=weight_lookup[val[0]]))
        if not vector:
            vector = SearchVector(relationship_name, weight=weight_lookup[val[0]])
        else:
            vector += SearchVector(relationship_name, weight=weight_lookup[val[0]])

    query = SearchQuery(keyword)

    if len(similarities) > 1:
        similarity = Greatest(*similarities)
    elif len(similarities) == 1:
        similarity = similarities[0]
    else:
        return model.objects.none()

    # results =  model.objects.annotate(
    results =  queryset.annotate(
        # search=vector,
        rank=SearchRank(vector,query),
        similarity=similarity
    ).filter(
        # Q(search__icontains=keyword) | # for some reason 'search=' in Q lose icontains abilities
        # Q(search=keyword) | # for some reason __icontains paired w/ Q misses perfect matches
        Q(rank__gt=settings.MIN_SEARCH_RANK) |
        Q(similarity__gt=settings.MIN_SEARCH_SIMILARITY)
    ).order_by(
        '-rank',
        '-similarity',
        sort_field
    )

    return results

def run_filters(request, providers):
    try:
        body = json.loads(request.body)
        for key in body.keys():
            if 'keywords' not in key:
                if len(body[key]) > 0 and type(body[key][0]) == str:
                    str_values = body[key]
                    body[key] = [int(x) for x in str_values]
    except Exception as e:
        print(e)
        body = {}

    filters = {}
    if 'product_categories' in body.keys():
        # Many-to-many (OR)
        filters['Product Types'] = []
        product_ids = []
        for filter_category in ProductCategory.objects.filter(pk__in=body['product_categories']):
            filters['Product Types'].append({'id': filter_category.pk, 'name': str(filter_category)})
            product_ids += [x.pk for x in filter_category.get_provider_products()]
        provider_products = ProviderProduct.objects.filter(pk__in=product_ids)
        provider_ids = [x.provider.pk for x in provider_products]
        providers = providers.filter(pk__in=provider_ids)
        filters['Product Types'].sort(key=lambda x: x['name'])
    if 'identities' in body.keys():
        # Many-to-many (OR)
        identities = Identity.objects.filter(pk__in=body['identities'])
        filters['Producer Identities'] = []
        provider_ids = []
        for identity in identities:
            filters['Producer Identities'].append({'id': identity.pk, 'name': str(identity)})
            new_provider_ids = [x.pk for x in identity.provider_set.all()]
            provider_ids = list(set(provider_ids + new_provider_ids))
        providers = providers.filter(pk__in=provider_ids)
        filters['Producer Identities'].sort(key=lambda x: x['name'])
    if 'availability' in body.keys():
        # Many-to-many (OR)
        regions = PoliticalSubregion.objects.filter(pk__in=body['availability'])
        filters['County Availability'] = []
        provider_ids = []
        for region in regions:
            filters['County Availability'].append({'id': region.pk, 'name': str(region)})
            new_provider_ids = [x.pk for x in region.provider_set.all()]
            provider_ids = list(set(provider_ids + new_provider_ids))
        providers = providers.filter(pk__in=provider_ids)
        filters['County Availability'].sort(key=lambda x: x['name'])
    if 'physical_counties' in body.keys():
        # Many-to-many (OR)
        regions = PoliticalSubregion.objects.filter(pk__in=body['physical_counties'])
        filters['Producer Counties'] = []
        provider_ids = []
        for region in regions:
            filters['Producer Counties'].append({'id': region.pk, 'name': str(region)})
            new_provider_ids = [x.pk for x in providers if x.locationCounty == region]
            provider_ids = list(set(provider_ids + new_provider_ids))
        providers = providers.filter(pk__in=provider_ids)
        filters['Producer Counties'].sort(key=lambda x: x['name'])
    if 'component_categories' in body.keys():
        # Many-to-many (OR)
        components = ComponentCategory.objects.filter(pk__in=body['component_categories'])
        filters['Meal Components'] = []
        provider_ids = []
        for component in components:
            filters['Meal Components'].append({'id': component.pk, 'name': str(component)})
            for provider in providers:
                if component in provider.components_offered and not provider.id in provider_ids:
                    provider_ids.append(provider.id)
        providers = providers.filter(pk__in=provider_ids)
        filters['Meal Components'].sort(key=lambda x: x['name'])
    if 'delivery_methods' in body.keys():
        # Many-to-many (OR)
        delivery_methods = DeliveryMethod.objects.filter(pk__in=body['delivery_methods'])
        filters['Delivery Methods'] = []
        provider_ids = []
        for method in delivery_methods:
            filters['Delivery Methods'].append({'id': method.pk, 'name': str(method)})
            new_provider_ids = [x.pk for x in method.provider_set.all()]
            provider_ids = list(set(provider_ids + new_provider_ids))
        providers = providers.filter(pk__in=provider_ids)
        filters['Delivery Methods'].sort(key=lambda x: x['name'])
    if 'distributors' in body.keys():
        # Many-to-many (OR)
        distributors = Distributor.objects.filter(pk__in=body['distributors'])
        filters['Distributors'] = []
        provider_ids = []
        for distributor in distributors:
            filters['Distributors'].append({'id': distributor.pk, 'name': str(distributor)})
            new_provider_ids = [x.pk for x in distributor.provider_set.all()]
            provider_ids = list(set(provider_ids + new_provider_ids))
        providers = providers.filter(pk__in=provider_ids)
        filters['Distributors'].sort(key=lambda x: x['name'])
    if 'practices' in body.keys():
        # Many-to-many (OR)
        practices = ProductionPractice.objects.filter(pk__in=body['practices'])
        filters['Practices'] = []
        provider_ids = []
        for practice in practices:
            filters['Practices'].append({'id': practice.pk, 'name': str(practice)})
            new_provider_ids = [x.pk for x in practice.provider_set.all()]
            provider_ids = list(set(provider_ids + new_provider_ids))
        providers = providers.filter(pk__in=provider_ids)
        filters['Practices'].sort(key=lambda x: x['name'])
    if 'languages' in body.keys():
        # Many-to-many (OR)
        languages = Language.objects.filter(pk__in=body['languages'])
        filters['Languages'] = []
        provider_ids = []
        for language in languages:
            filters['Languages'].append({'id': language.pk, 'name': str(language)})
            new_provider_ids = [x.pk for x in language.provider_set.all()]
            provider_ids = list(set(provider_ids + new_provider_ids))
        providers = providers.filter(pk__in=provider_ids)
        filters['Languages'].sort(key=lambda x: x['name'])
    if 'product_forms' in body.keys():
        product_forms = ProductCategory.objects.filter(pk__in=body['product_forms'])
        filters['Product Forms'] = []
        provider_ids = []
        for form in product_forms:
            filters['Product Forms'].append({'id': form.pk, 'name': str(form)})
            # TODO: How strict are the 'product details' filters? Should "Poultry > Chicken" get
            # any/all forms of chicken, or only those that specifically set this 'type'.
            # Current solution: take 'Poultry > Chicken' to be inclusive of all decendants.
            # new_provider_ids = [x.pk for x in providers.filter(providerproduct__category=form)]
            new_provider_ids = [x.provider.pk for x in form.get_provider_products()]
            provider_ids = list(set(provider_ids + new_provider_ids))
        providers = providers.filter(pk__in=provider_ids)
        filters['Product Forms'].sort(key=lambda x: x['name'])
    if 'keywords' in body.keys():
        # recreate the trigram keyword search from ITKDB
        # https://github.com/Ecotrust/TEKDB/blob/main/TEKDB/TEKDB/models.py#L23
        # This is run on both "Provider" and "ProviderProduct"

        # This will be different, as we want to apply the above filters to 
        # constrain the search space.

        # enable Trigram Similarity extension on PG if not done already
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')

        keywords = body['keywords']

        # model = Provider
        fields = [
            'name', 
            'description', 
            'primaryContactFirstName', 
            'primaryContactLastName', 
            'notes',
        ]
        # We do not search all FK fields - these searches are expensive/slow, and should be managed
        # via the existing filters.
        fk_fields=[
            # ('preferredLanguage', 'name'),
            # ('identities',  'name'),
            # ('deliveryMethods', 'name'),
            ('regionalAvailability', 'name'),
            # ('distributors', 'name'),
            # ('productionPractices', 'name'),
        ]
        weight_lookup = {
            'name': 'A',
            'description': 'C',
            'primaryContactFirstName': 'C',
            'primaryContactLastName': 'C',
            'notes': 'C',
            'preferredLanguage': 'B',
            'identities': 'B',
            'deliveryMethods': 'B',
            'regionalAvailability': 'B',
            'distributors': 'B',
            'productionPractices': 'B',
        }

        sort_field = 'name'

        keyword_providers = run_keyword_search(providers, Provider, keywords, fields, fk_fields, weight_lookup, sort_field)

        # model = ProviderProduct
        fields = [
            'name', 
            'description',
            'notes',
        ]
        fk_fields=[
            ('category', 'full_name'),
            # ('deliveryMethods', 'name'),
            ('regionalAvailability', 'name'),
            # ('distributors', 'name'),
            # ('productionPractices', 'name'),
        ]
        weight_lookup = {
            'name': 'A',
            'category': 'A',
            'description': 'C',
            'notes': 'C',
            'deliveryMethods': 'B',
            'regionalAvailability': 'B',
            'distributors': 'B',
            'productionPractices': 'B',
        }
        products = ProviderProduct.objects.filter(provider__in=providers)
        keyword_provider_products = run_keyword_search(products, ProviderProduct, keywords, fields, fk_fields, weight_lookup, sort_field)

        provider_results = []
        provider_ids = []
        for provider in keyword_providers:
            provider_results.append({
                'id': provider.pk,
                'name': provider.name,
                'rank': provider.rank,
                'similarity': provider.similarity
            })
        for product in keyword_provider_products:
            provider_results.append({
                'id': product.provider.pk,
                'name': product.provider.name,
                'rank': product.rank,
                'similarity': product.similarity
            })
        
        # If searching by keyword, results should be sorted by rank. Similarity if there is a tie in rank. 
        # Name if there is a tie between both.
        provider_results.sort(key=lambda x: x['name'])
        provider_results.sort(key=lambda x: x['similarity'], reverse=True)
        provider_results.sort(key=lambda x: x['rank'], reverse=True)


        # print("\n")
        # print("============================================")
        # print("----------Providers---------------")
        # print("============================================")
        # print("ID \t NAME \t RANK \t SIMILARITY")
        # for result in [(x['id'], x['name'], x['rank'], x['similarity']) for x in provider_results]:
        #     print(result)
        # print("============================================")
        # print("\n")


        for provider in provider_results:
            if not provider['id'] in provider_ids:
                provider_ids.append(provider['id'])

        preserved_order = Case(*[When(pk=id, then=index) for index, id in enumerate(provider_ids)])
        providers = providers.filter(pk__in=provider_ids).order_by(preserved_order)

    return {
        'providers': providers,
        'filters': filters
    }

#   requests should have a 'filters' object that gets parsed, run against the
# providers records, then an alphabetical list of results should be put into
# the JsonResponse and sent back to the client to render.
def filter(request):
    providers = Provider.objects.all()
    if request.method == "POST":
        filter_results = run_filters(request, providers)
        providers = filter_results['providers']
        filters = filter_results['filters']

    providers_response = {'providers': []}
    for p in providers:
      providers_response['providers'].append({
        'id': p.id,
        'name': p.name,
        'businessAddressCity': p.businessAddressCity,
        'businessAddressState': {
            'initialism': p.businessAddressState.initialism
        },
        'product_categories': [{'image':x['object'].image_string} for x in p.product_categories]
      })

    filters_response = [x for x in request.POST.keys()][0]

    data = [providers_response, filters_response, filters]
    return JsonResponse(data, safe=False)

def printer_friendly_results(request):
    providers = [{'name':''}]
    filter_list = []
    if request.method == "POST":
        providers = Provider.objects.all()
        filter_response = run_filters(request, providers)
        providers =  filter_response['providers']
        filters = filter_response['filters']
        filter_keys = [x for x in filter_response['filters'].keys()]
        filter_keys.sort()
        for key in filter_keys:
            filter_list.append({
                'name': key,
                'list': ', '.join([x['name'] for x in filters[key]])
            })

    context = {
        'providers': providers,
        'filter_list': filter_list
    }

    return render(request, "printable_results.html", context)
