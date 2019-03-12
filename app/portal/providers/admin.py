from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import PoliticalRegion, PoliticalSubregion, DeliveryMethod, DeliveryMethod, Distributor, Provider, CapacityMeasurement, ProductCategory, Product, ProviderProduct, Identity, ProductionPractice

# class ProductInline(admin.StackedInline):
class ProductInline(admin.TabularInline):
    filter_horizontal = ('deliveryMethods', 'regionalAvailability', 'distributors', 'productionPractices')
    model = ProviderProduct
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'category',
                'description',
            )
        }),
        ('Liability', {
            'fields': (
                ('productLiabilityInsurance', 'productLiabilityInsuranceAmount',),
            )
        }),
        ('Availability', {
            'fields': (
                'deliveryMethods',
                'regionalAvailability',
                ('orderMinimum', 'deliveryMinimum',),
                'distributors',
            )
        }),
        ('Additional Info', {
            'fields': (
                'productionPractices',
                ('capacityValue', 'capacityMeasurement',),
                # 'image',
                'notes',
            )
        }),

    )

class ProviderAdmin(admin.ModelAdmin):
    filter_horizontal = ('identities', 'deliveryMethods', 'regionalAvailability', 'distributors', 'productionPractices')

    list_display = ('name','outreachConductor','businessAddressCity',
    'businessAddressState','soldToSchoolsBefore','dateInfoUpdated')
    search_fields = ('name','outreachConductor','businessAddressCity',
    'businessAddressState','soldToSchoolsBefore','dateInfoUpdated')
    readonly_fields = ('dateInfoUpdated'),

    inlines = [
        ProductInline,
    ]

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     provider = Provider.objects.get(pk=object_id)
    #     extra_context['provider'] = provider
    #     extra_context['products'] = provider.providerproduct_set.all()
    #     return super().change_view(
    #         request, object_id, form_url, extra_context=extra_context,
    #     )

    fieldsets = (
        (None, {
            # 'classes': ('producer-name',),
            'fields': (
                'name',
                ('outreachConductor', 'dateInfoUpdated',),
                'soldToSchoolsBefore',
                'description',
                ('primaryContactFirstName', 'primaryContactLastName',),
            )
        }),
        ('Business Address', {
            'fields': (
                'businessAddressLine1',
                'businessAddressLine2',
                ('businessAddressCity', 'businessAddressState', 'businessAddressZipCode',),
            )
        }),
        ('Physical Address', {
            'fields': (
                'physicalAddressIsSame',
                'physicalAddressLine1',
                'physicalAddressLine2',
                ('physicalAddressCity', 'physicalAddressState', 'physicalAddressZipCode',),
            )
        }),
        ('Contact Info', {
            'fields': (
                ('officePhone', 'cellPhone',),
                'email',
                'websiteAddress',
            )
        }),
        ('Liability', {
            'fields': (
                ('productLiabilityInsurance', 'productLiabilityInsuranceAmount',),
            )
        }),
        ('Availability', {
            'fields': (
                'deliveryMethods',
                'regionalAvailability',
                ('orderMinimum', 'deliveryMinimum',),
                'distributors',
            )
        }),
        ('Additional Info', {
            'fields': (
                'productionPractices',
                'identities',
                'notes',
            )
        }),
        # ('Products', {
        #     'fields': (
        #         'product_inline',
        #     )
        # }),
    )

    # add_form_template = '%s/TEKDB/templates/admin/CitationsForm.html' % BASE_DIR
    # change_form_template = 'admin/ProviderForm.html'

# class ProductAdmin(admin.ModelAdmin):
#
#     def add_view(self, request, form_url='', extra_context=None):
#         from urllib.parse import urlparse, parse_qs
#         extra_context = extra_context or {}
#         # import ipdb; ipdb.set_trace()
#         querystring = urlparse(request.get_raw_uri()).query
#         if '_provider' in parse_qs(querystring).keys():
#             try:
#                 extra_context['provider'] = int(parse_qs(querystring)['_provider'])
#             except Exception as e:
#                 pass
#         return super().add_view(
#             request, form_url, extra_context=extra_context,
#         )
#
#     # add_form_template = 'admin/ProductForm.html'


admin.site.register(PoliticalRegion)
admin.site.register(PoliticalSubregion)
admin.site.register(DeliveryMethod)
admin.site.register(Distributor)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(CapacityMeasurement)
admin.site.register(ProductCategory)
# admin.site.register(Product)
admin.site.register(ProviderProduct)
# admin.site.register(ProviderProduct, ProductAdmin)
admin.site.register(Identity)
admin.site.register(ProductionPractice)
