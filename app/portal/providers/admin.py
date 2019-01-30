from django.contrib import admin

from .models import PoliticalRegion, PoliticalSubregion, DeliveryMethod, DeliveryMethod, Distributor, Provider, CapacityMeasurement, ProductCategory, Product, ProviderProduct, Identity, ProductionPractice

admin.site.register(PoliticalRegion)
admin.site.register(PoliticalSubregion)
admin.site.register(DeliveryMethod)
admin.site.register(Distributor)
admin.site.register(Provider)
admin.site.register(CapacityMeasurement)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProviderProduct)
admin.site.register(Identity)
admin.site.register(ProductionPractice)
