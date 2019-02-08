from django.contrib import admin

from .models import PoliticalRegion, PoliticalSubregion, DeliveryMethod, DeliveryMethod, Distributor, Provider, CapacityMeasurement, ProductCategory, Product, ProviderProduct, Identity, ProductionPractice

# class ProductInline(admin.StackedInline):
class ProductInline(admin.TabularInline):
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
                'image',
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
        ('Physical Address', {
            'fields': (
                'physicalAddressIsSame',
                'physicalAddressLine1',
                'physicalAddressLine2',
                ('physicalAddressCity', 'physicalAddressState', 'physicalAddressZipCode',),
            )
        }),
        ('Business Address', {
            'fields': (
                'businessAddressLine1',
                'businessAddressLine2',
                ('businessAddressCity', 'businessAddressState', 'businessAddressZipCode',),
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
    )

    # add_form_template = '%s/TEKDB/templates/admin/CitationsForm.html' % BASE_DIR
    # change_form_template = '%s/TEKDB/templates/admin/CitationsForm.html' % BASE_DIR


admin.site.register(PoliticalRegion)
admin.site.register(PoliticalSubregion)
admin.site.register(DeliveryMethod)
admin.site.register(Distributor)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(CapacityMeasurement)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProviderProduct)
admin.site.register(Identity)
admin.site.register(ProductionPractice)
