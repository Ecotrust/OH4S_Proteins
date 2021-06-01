import json, datetime, statistics
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from django.http import HttpRequest
from providers.views import filter, get_homepage_filter_context, get_results_filter_context
from providers.models import *
import json

class FilterTestCase(TestCase):
    # def setUp(self):
    #     print('=====================')
    #     print('FilterTestCase: setUp')
    #     print('=====================')
    #
    #     user = User.objects.create(username='user')
    #     user.save()

    # Import fixture
    fixture_file = '/usr/local/apps/OH4S_Proteins/app/portal/fixtures/providers_20210524.json'
    # call_command('loaddata', fixture_file)
    fixtures = [fixture_file,]

    # Create a request with a filter fixture
    # - send request to /providers/filter
    # - parse JsonResponse into dict
    # - return dict
    def filter_request(self, filter_json_list):
        request = HttpRequest()
        request.method = 'POST'
        request.META['CONTENT_TYPE'] = 'application/json'
        data = {}
        for filter_obj in filter_json_list:
            data[filter_obj['key']] = filter_obj['value']
        request._body = json.dumps(data)
        results = filter(request)
        [providers_response, filters_reponse] = json.loads(results.content)
        return providers_response

    def test_fixtres(self):
        # self.assertTrue(Project.objects.all().count() > 0)
        self.assertTrue(PoliticalRegion.objects.all().count() > 0)
        self.assertTrue(PoliticalSubregion.objects.all().count() > 0)
        self.assertTrue(DeliveryMethod.objects.all().count() > 0)
        self.assertTrue(Distributor.objects.all().count() > 0)
        self.assertTrue(Identity.objects.all().count() > 0)
        self.assertTrue(ProductionPractice.objects.all().count() > 0)
        self.assertTrue(CapacityMeasurement.objects.all().count() > 0)
        # self.assertTrue(CategoryManager.objects.all().count() > 0)
        self.assertTrue(ProductCategory.objects.all().count() > 0)
        # self.assertTrue(Product.objects.all().count() > 0)
        self.assertTrue(ProviderProduct.objects.all().count() > 0)

    def test_homepage_filters_category(self):
        # Create json filter object
        # - Get dict of response from filter query
        # - Check dict for correct results
        # - (Only those matching provided category)
        apples_category = ProductCategory.objects.get(name='Apples')
        json_filters = [
            {
                'key': 'product_categories',
                'value': [
                    apples_category.pk, # 34
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('product_categories' in  provider.keys())
            product_ids = [x['id'] for x in provider['product_categories']]
            self.assertTrue(apples_category.pk in product_ids)

    def test_homepage_filters_identity(self):
        # Create json filter object
        # - Get dict of response from filter query
        # - Check dict for correct results
        # - (Only those matching provided identity)
        minority_identity = Identity.objects.get(name='Minority Owned')
        json_filters = [
            {
                'key': 'identities',
                'value': [
                    minority_identity.pk,
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('identities' in  provider.keys())
            identity_ids = [x['id'] for x in provider['identities']]
            self.assertTrue(minority_identity.pk in identity_ids)

    def test_homepage_filters_county(self):
        # Create json filter object
        # - Get dict of response from filter query
        # - Check dict for correct results
        # - (Only those matching provided county of availability)
        benton_county = PoliticalSubregion.objects.get(name='Benton')
        json_filters = [
            {
                'key': 'availability',
                'value': [
                    benton_county.pk,
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('regionalAvailability' in  provider.keys())
            county_ids = [x['id'] for x in provider['regionalAvailability']]
            self.assertTrue(benton_county.pk in county_ids)

    def test_homepage_filters_component(self):
        # Create json filter object
        # - Get dict of response from filter query
        # - Check dict for correct results
        # - (Only those matching provided component category)
        meats = ComponentCategory.objects.get(name='Meats / Meat Alternates')
        json_filters = [
            {
                'key': 'component_categories',
                'value': [
                    meats.pk,
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('products' in  provider.keys())
            self.assertTrue(len(provider['products']) > 0)
            self.assertTrue('category' in  provider['products'][0].keys())
            self.assertTrue('usdaComponentCategories' in  provider['products'][0]['category'].keys())
            component_ids = []
            for product in provider['products']:
                component_ids = component_ids + [x['id'] for x in product['category']['usdaComponentCategories']]
            self.assertTrue(meats.pk in component_ids)

    def test_homepage_filters_composite(self):
        # Create json filter object
        # - Get dict of response from filter query
        # - Check dict for correct results
        # - (Only those matching provided filters)
        clatsop = PoliticalSubregion.objects.get(name='Clatsop')
        tillamook = PoliticalSubregion.objects.get(name='Tillamook')
        women = Identity.objects.get(name='Women-Owned')
        lgbtq = Identity.objects.get(name='LGBTQ-Owned')
        beets = ProductCategory.objects.get(name='Beets')
        broccoli = ProductCategory.objects.get(name='Broccoli')
        veggies = ComponentCategory.objects.get(name='Vegetables')
        json_filters = [
            {
                'key': 'availability',
                'value': [
                    clatsop.pk,
                    tillamook.pk
                ]
            },
            {
                'key': "identities",
                'value': [
                    women.pk,
                    lgbtq.pk
                ]
            },
            {
                'key': "product_categories",
                'value': [
                    beets.pk,
                    broccoli.pk
                ]
            },
            {
                'key': 'component_categories',
                'value': [
                    veggies.pk,
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('regionalAvailability' in  provider.keys())
            county_ids = [x['id'] for x in provider['regionalAvailability']]
            self.assertTrue(clatsop.pk in county_ids)
            self.assertTrue(tillamook.pk in county_ids)
            self.assertTrue('identities' in  provider.keys())
            identity_ids = [x['id'] for x in provider['identities']]
            self.assertTrue(women.pk in identity_ids)
            self.assertTrue(lgbtq.pk in identity_ids)
            self.assertTrue('product_categories' in  provider.keys())
            product_ids = [x['id'] for x in provider['product_categories']]
            self.assertTrue(beets.pk in product_ids)
            self.assertTrue(broccoli.pk in product_ids)
            self.assertTrue(len(provider['products']) > 0)
            self.assertTrue('category' in  provider['products'][0].keys())
            self.assertTrue('usdaComponentCategories' in  provider['products'][0]['category'].keys())
            component_ids = []
            for product in provider['products']:
                component_ids = component_ids + [x['id'] for x in product['category']['usdaComponentCategories']]
            self.assertTrue(veggies.pk in component_ids)

    def test_results_filters(self):
        # Create json filter object
        # - Get dict of response from filter query
        # - Check dict for correct results
        # - (Only those matching provided category)

        # PRODUCT TYPE
        asparagus_category = ProductCategory.objects.get(name='Asparagus')
        json_filters = [
            {
                'key': 'product_categories',
                'value': [
                    asparagus_category.pk,
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('product_categories' in  provider.keys())
            product_ids = [x['id'] for x in provider['product_categories']]
            self.assertTrue(asparagus_category.pk in product_ids)

        # PRODUCER LOCATION
        deschutes = PoliticalSubregion.objects.get(name='Deschutes')
        json_filters = [
            {
                'key': 'physical_counties',
                'value': [
                    deschutes.pk,
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('physicalCounty' in  provider.keys())
            self.assertTrue(None != provider['physicalCounty'])
            self.assertTrue('id' in provider['physicalCounty'].keys())
            self.assertTrue(deschutes.pk == provider['physicalCounty']['id'])

        # DELIVERY METHOD
        supplier_delivers = DeliveryMethod.objects.get(name='Supplier Delivers')
        json_filters = [
            {
                'key': 'delivery_methods',
                'value': [
                    supplier_delivers.pk,   #1
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('deliveryMethods' in  provider.keys())
            product_ids = [x['id'] for x in provider['deliveryMethods']]
            self.assertTrue(supplier_delivers.pk in product_ids)

        # PRODUCT DETAILS
        carrots = ProductCategory.objects.get(name='Carrots')
        fresh_carrots = ProductCategory.objects.get(name='Fresh, whole', parent=carrots)
        json_filters = [
            {
                'key': 'product_forms',
                'value': [
                    fresh_carrots.pk,
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('products' in  provider.keys())
            self.assertTrue('product_categories' in  provider.keys())
            product_ids = [x['category']['id'] for x in provider['products']]
            category_ids = [x['id'] for x in provider['product_categories']]
            self.assertTrue(fresh_carrots.pk in product_ids)
            self.assertTrue(carrots.pk in category_ids)

        # DISTRIBUTORS
        sysco = Distributor.objects.get(name='Sysco')
        json_filters = [
            {
                'key': 'distributors',
                'value': [
                    sysco.pk,
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('distributors' in  provider.keys())
            product_ids = [x['id'] for x in provider['distributors']]
            self.assertTrue(sysco.pk in product_ids)

        # PRODUCTION PRACTICES
        orTilth = ProductionPractice.objects.get(name='Oregon Tilth')
        json_filters = [
            {
                'key': 'practices',
                'value': [
                    orTilth.pk,
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('productionPractices' in  provider.keys())
            product_ids = [x['id'] for x in provider['productionPractices']]
            self.assertTrue(orTilth.pk in product_ids)

    def test_get_home_filter_context(self):
        request = HttpRequest()
        request.path = '/'
        request.method = 'GET'
        context = get_homepage_filter_context(request, {})

        self.assertTrue('filters' in context.keys())
        self.assertEqual(3, len(context['filters']))

        # Producer Identity
        identity_filter = context['filters'][0]
        self.assertTrue('name' in identity_filter.keys())
        self.assertEqual('Producer Identity', identity_filter['name'])
        self.assertTrue('facet' in identity_filter.keys())
        self.assertEqual('identities', identity_filter['facet'])
        self.assertTrue('widget' in identity_filter.keys())
        self.assertEqual('multiselect', identity_filter['widget'])
        self.assertTrue('options' in identity_filter.keys())
        self.assertEqual(Identity.objects.all().count(), len(identity_filter['options']))
        self.assertEqual(type(identity_filter['options'][0]['value']), int)
        self.assertEqual(type(identity_filter['options'][0]['label']), str)
        self.assertEqual(type(identity_filter['options'][0]['state']), bool)

        # County Availability
        county_filter = context['filters'][1]
        self.assertTrue('name' in county_filter.keys())
        self.assertEqual('Availability By County', county_filter['name'])
        self.assertTrue('facet' in county_filter.keys())
        self.assertEqual('availability', county_filter['facet'])
        self.assertTrue('widget' in county_filter.keys())
        self.assertEqual('multiselect-spatial', county_filter['widget'])
        self.assertTrue('data-layer' in county_filter.keys())
        # TODO: Add datalayer (json/svg filename) to be passed to front-end map with selection
        self.assertTrue('options' in county_filter.keys())
        self.assertEqual(PoliticalSubregion.objects.all().count(), len(county_filter['options']))
        self.assertEqual(type(county_filter['options'][0]['value']), int)
        self.assertEqual(type(county_filter['options'][0]['label']), str)
        self.assertEqual(type(county_filter['options'][0]['state']), bool)

        # USDA Meal Components
        component_filter = context['filters'][2]
        self.assertTrue('name' in component_filter.keys())
        self.assertEqual('USDA Meal Components', component_filter['name'])
        self.assertTrue('facet' in component_filter.keys())
        self.assertEqual('component_categories', component_filter['facet'])
        self.assertTrue('widget' in component_filter.keys())
        self.assertEqual('multiselect', component_filter['widget'])
        self.assertTrue('options' in component_filter.keys())
        self.assertEqual(ComponentCategory.objects.all().count(), len(component_filter['options']))
        self.assertEqual(type(component_filter['options'][0]['value']), int)
        self.assertEqual(type(component_filter['options'][0]['label']), str)
        self.assertEqual(type(component_filter['options'][0]['state']), bool)


    def test_get_results_filter_context(self):
        EXPECTED_FILTER_COUNT = 9
        LOCATION_FILTER_INDEX = 3
        DELIVERY_FILTER_INDEX = LOCATION_FILTER_INDEX + 1
        CATEGORY_FILTER_INDEX = LOCATION_FILTER_INDEX + 2
        FORM_FILTER_INDEX = LOCATION_FILTER_INDEX + 3
        DISTRIBUTOR_FILTER_INDEX = LOCATION_FILTER_INDEX + 4
        PRACTICE_FILTER_INDEX = LOCATION_FILTER_INDEX + 5
        request = HttpRequest()
        request.path = '/results'
        request.method = 'POST'
        request.META['CONTENT_TYPE'] = 'application/json'
        data = {}
        # for filter_obj in filter_json_list:
        #     data[filter_obj['key']] = filter_obj['value']
        request._body = json.dumps(data)
        context = get_results_filter_context(request)

        self.assertTrue('filters' in context.keys())
        self.assertEqual(len(context['filters']), EXPECTED_FILTER_COUNT)

        # Producer Location
        location_filters = context['filters'][LOCATION_FILTER_INDEX]
        self.assertTrue('name' in location_filters.keys())
        self.assertEqual('Producer Location', location_filters['name'])
        self.assertTrue('facet' in location_filters.keys())
        self.assertEqual('physical_counties', location_filters['facet'])
        self.assertTrue('widget' in location_filters.keys())
        self.assertEqual('multiselect-spatial', location_filters['widget'])
        self.assertTrue('data-layer' in location_filters.keys())
        # TODO: Add datalayer (json/svg filename) to be passed to front-end map with selection
        self.assertTrue('options' in location_filters.keys())
        self.assertEqual(PoliticalSubregion.objects.all().count(), len(location_filters['options']))
        self.assertEqual(type(location_filters['options'][LOCATION_FILTER_INDEX]['value']), int)
        self.assertEqual(type(location_filters['options'][LOCATION_FILTER_INDEX]['label']), str)
        self.assertEqual(type(location_filters['options'][LOCATION_FILTER_INDEX]['state']), bool)

        # Delivery Method
        delivery_filters = context['filters'][DELIVERY_FILTER_INDEX]
        self.assertTrue('name' in delivery_filters.keys())
        self.assertEqual('Delivery Method', delivery_filters['name'])
        self.assertTrue('facet' in delivery_filters.keys())
        self.assertEqual('delivery_methods', delivery_filters['facet'])
        self.assertTrue('widget' in delivery_filters.keys())
        self.assertEqual('multiselect', delivery_filters['widget'])
        self.assertTrue('options' in delivery_filters.keys())
        self.assertEqual(DeliveryMethod.objects.all().count(), len(delivery_filters['options']))
        self.assertEqual(type(delivery_filters['options'][0]['value']), int)
        self.assertEqual(type(delivery_filters['options'][0]['label']), str)
        self.assertEqual(type(delivery_filters['options'][0]['state']), bool)

        # Product Type (Category)
        category_filters = context['filters'][CATEGORY_FILTER_INDEX]
        self.assertTrue('name' in category_filters.keys())
        self.assertEqual('Product Type', category_filters['name'])
        self.assertTrue('facet' in category_filters.keys())
        self.assertEqual('product_categories', category_filters['facet'])
        self.assertTrue('widget' in category_filters.keys())
        self.assertEqual('multiselect', category_filters['widget'])
        self.assertTrue('options' in category_filters.keys())
        self.assertEqual(ProductCategory.objects.filter(parent=None).count(), len(category_filters['options']))
        self.assertEqual(type(category_filters['options'][0]['value']), int)
        self.assertEqual(type(category_filters['options'][0]['label']), str)
        self.assertEqual(type(category_filters['options'][0]['state']), bool)

        # Product Details (Form)
        details_filters = context['filters'][FORM_FILTER_INDEX]
        self.assertTrue('name' in details_filters.keys())
        self.assertEqual('Product Details', details_filters['name'])
        self.assertTrue('facet' in details_filters.keys())
        self.assertEqual('product_forms', details_filters['facet'])
        self.assertTrue('widget' in details_filters.keys())
        # TODO: Determine if A: this always shows, B: this is hierarchical, or C: this is merged with Product Type
        self.assertEqual('multiselect', details_filters['widget'])
        self.assertTrue('options' in details_filters.keys())
        self.assertEqual(ProductCategory.objects.exclude(parent=None).count(), len(details_filters['options']))
        self.assertEqual(type(details_filters['options'][0]['value']), int)
        self.assertEqual(type(details_filters['options'][0]['label']), str)
        self.assertEqual(type(details_filters['options'][0]['state']), bool)

        # Distributors
        distributor_filters = context['filters'][DISTRIBUTOR_FILTER_INDEX]
        self.assertTrue('name' in distributor_filters.keys())
        self.assertEqual('Distributors', distributor_filters['name'])
        self.assertTrue('facet' in distributor_filters.keys())
        self.assertEqual('distributors', distributor_filters['facet'])
        self.assertTrue('widget' in distributor_filters.keys())
        self.assertEqual('multiselect', distributor_filters['widget'])
        self.assertTrue('options' in distributor_filters.keys())
        self.assertEqual(Distributor.objects.all().count(), len(distributor_filters['options']))
        self.assertEqual(type(distributor_filters['options'][0]['value']), int)
        self.assertEqual(type(distributor_filters['options'][0]['label']), str)
        self.assertEqual(type(distributor_filters['options'][0]['state']), bool)

        # Production Practices
        practice_filters = context['filters'][PRACTICE_FILTER_INDEX]
        self.assertTrue('name' in practice_filters.keys())
        self.assertEqual('Production Practices', practice_filters['name'])
        self.assertTrue('facet' in practice_filters.keys())
        self.assertEqual('practices', practice_filters['facet'])
        self.assertTrue('widget' in practice_filters.keys())
        self.assertEqual('multiselect', practice_filters['widget'])
        self.assertTrue('options' in practice_filters.keys())
        self.assertEqual(ProductionPractice.objects.all().count(), len(practice_filters['options']))
        self.assertEqual(type(practice_filters['options'][0]['value']), int)
        self.assertEqual(type(practice_filters['options'][0]['label']), str)
        self.assertEqual(type(practice_filters['options'][0]['state']), bool)
