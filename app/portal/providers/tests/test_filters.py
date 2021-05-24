import json, datetime, statistics
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from django.http import HttpRequest
from providers.views import filter
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
                'key': 'component_category',
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
                'key': 'component_category',
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
                    asparagus_category.pk, # 34
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('product_categories' in  provider.keys())
            product_ids = [x['id'] for x in provider['product_categories']]
            self.assertTrue(asparagus_category.pk in product_ids)

        # PRODUCER LOCATION
        print("TODO: Filter by producer location")

        # DELIVERY METHOD
        supplier_delivers = DeliveryMethod.objects.get(name='Supplier Delivers')
        json_filters = [
            {
                'key': 'delivery_method',
                'value': [
                    supplier_delivers.pk,   #1
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('delivery_method' in  provider.keys())
            product_ids = [x['id'] for x in provider['delivery_method']]
            self.assertTrue(supplier_delivers.pk in product_ids)

        # PRODUCT DETAILS
        print("TODO: Filter by product details")

        # DISTRIBUTORS
        sysco = Distributor.objects.get(name='Sysco')
        json_filters = [
            {
                'key': 'distributor',
                'value': [
                    sysco.pk,
                ]
            }
        ]
        results = self.filter_request(json_filters)
        for provider in results['providers']:
            self.assertTrue('distributor' in  provider.keys())
            product_ids = [x['id'] for x in provider['distributor']]
            self.assertTrue(sysco.pk in product_ids)

        # PRODUCTION PRACTICES
        orTilth = ProductionPractices.objects.get(name='Oregon Tilth')
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
            self.assertTrue('practices' in  provider.keys())
            product_ids = [x['id'] for x in provider['practices']]
            self.assertTrue(orTilth.pk in product_ids)
