from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import PoliticalRegion, PoliticalSubregion, DeliveryMethod, DeliveryMethod, Distributor, Provider, CapacityMeasurement, ComponentCategory, ProductCategory, Product, ProviderProduct, Identity, ProductionPractice, School, Language, ContactMethod

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
                'packSize',
                'notes',
            )
        }),

    )

class ProviderAdmin(admin.ModelAdmin):
    filter_horizontal = ('schoolsSoldTo', 'identities', 'deliveryMethods', 'regionalAvailability', 'distributors', 'productionPractices', 'preferredLanguage', 'preferredContactMethod')

    list_display = ('name','outreachConductor','businessAddressCity',
    'businessAddressState','soldToSchoolsBefore','dateInfoUpdated')
    search_fields = (
        'name',
        'outreachConductor',
        'businessAddressCity',
        'businessAddressState__name',
        'businessAddressState__initialism',
        'soldToSchoolsBefore',
    )
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
        ('Contact Info', {
            # 'classes': ('producer-name',),
            'fields': (
                'name',
                ('primaryContactFirstName', 'primaryContactLastName',),
                'email',
                ('officePhone', 'cellPhone',),
                'preferredContactMethod',
                'description',
                'websiteAddress',
                'soldToSchoolsBefore',
                'schoolsSoldTo',
                
            )
        }),
        ('Physical Business Details', {
            'fields': (
                'businessAddressLine1',
                'businessAddressLine2',
                ('businessAddressCity', 'businessAddressState', 'businessAddressZipCode',),
                'businessCounty',
                'productionPractices',
            )
        }),
        ('Physical Address', {
            'fields': (
                'physicalAddressIsSame',
                'physicalAddressLine1',
                'physicalAddressLine2',
                ('physicalAddressCity', 'physicalAddressState', 'physicalAddressZipCode',),
                'physicalCounty'
            )
        }),
        ('Liability', {
            'fields': (
                ('productLiabilityInsurance', 'productLiabilityInsuranceAmount',),
            )
        }),
        ('Availability', {
            'fields': (
                'regionalAvailability',
                'deliveryMethods',
                'distributors',
                # ('orderMinimum', 'deliveryMinimum',),
                'orderMinimum',
            )
        }),
        ('Preferred Language', {
            'fields': (
                'preferredLanguage',
            )
        }),
        ('Self-Identification', {
            'fields': (
                'identities',
                'notes',
            )
        }),
        ('Outreach', {
            'fields': (
                'outreachConductor',
                'dateInfoUpdated',
            )
        })
    )


class CategoryForm(forms.ModelForm):
    class Meta:
        exclude = ('pk',)
        model = ProductCategory
        widgets = {
            'usdaComponentCategories': admin.widgets.FilteredSelectMultiple('ComponentCategory', False),
        }

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('full_name', 'capacityMeasurement__unit', 'image')
    list_display = ('full_name','capacityMeasurement','image')
    form = CategoryForm

admin.site.register(School)
admin.site.register(Language)
admin.site.register(ContactMethod)
admin.site.register(PoliticalRegion)
admin.site.register(PoliticalSubregion)
admin.site.register(DeliveryMethod)
admin.site.register(Distributor)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(CapacityMeasurement)
admin.site.register(ComponentCategory)
admin.site.register(ProductCategory, CategoryAdmin)
# admin.site.register(Product)
admin.site.register(ProviderProduct)
# admin.site.register(ProviderProduct, ProductAdmin)
admin.site.register(Identity)
admin.site.register(ProductionPractice)
