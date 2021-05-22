from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField

class Project(models.Model):
    name = models.CharField(max_length=255, default="Oregon Harvest For Schools")
    welcome = models.TextField(null=True, blank=True, default=None)
    logo = models.ImageField(null=True, blank=True, default=None, upload_to='logo_images')

    def __str__(self):
        return self.name

# Filter Model? Can we let Admin craft her own filters? Seems unlikely...

class PoliticalRegion(models.Model):
    REGION_TYPE_CHOICES = (
        ('State', 'State'),
        ('Province', 'Province'),           # British Columbia Province, CA
        ('Commonwealth', 'Commonwealth'),   # Commonwealth of Virginia
        ('District', 'District'),       # District of Columbia
        ('Territory', 'Territory'),
        ('Other', 'Other'),
    )
    initialism = models.CharField(max_length=4, verbose_name="Initials", help_text="i.e. 'OR' for 'Oregon'. No periods.")
    name = models.CharField(max_length=100, verbose_name="Full Name")
    country = models.CharField(max_length=150, default='USA', help_text="Default is 'USA'")
    regionType = models.CharField(max_length=30, choices=REGION_TYPE_CHOICES, default='State', verbose_name="Type of political region")

    def __str__(self):
        if self.country.lower() == 'usa' or 'united states' in self.country.lower():
            if self.regionType == 'State':
                return "%s: %s" % (self.initialism, self.name)
            else:
                return "%s: %s of %s" % (self.initialism, self.regionType, self.name)
        return "%s: %s %s, %s" % (self.initialism, self.name, self.regionType, self.country)

    def to_dict(self):
        return {
            'id': self.id,
            'initialism': self.initialism,
            'name': self.name,
            'country': self.country,
            'regionType': self.regionType
        }

    class Meta:
        ordering = ('name', 'country', )

class PoliticalSubregion(models.Model):
    SUBREGION_TYPE_CHOICES = (
        ('County', 'County'),
        ('City', 'City'),
        ('Municipality', 'Municipality'),
        ('District', 'District'),
        ('Other', 'Other'),
    )
    name = models.CharField(max_length=255)
    region = models.ForeignKey(PoliticalRegion, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name,
            'region': self.region.to_dict()
        }

    class Meta:
        ordering = ('name', 'region',)

class DeliveryMethod(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name
        }

    class Meta:
        ordering = ('name',)

class Distributor(models.Model):
    name = models.CharField(max_length=255)
    phone = PhoneNumberField(blank=True, null=True, default=None)
    email = models.EmailField(max_length=255, null=True, blank=True, default=None)
    websiteAddress = models.URLField(max_length=255, null=True, blank=True, default=None, help_text="Try to include either http:// (good) or https:// (better if available)")
    fax = PhoneNumberField(blank=True, null=True, default=None)
    primaryContactFirstName = models.CharField(max_length=100, blank=True, null=True, default=None, verbose_name="Primary contact's first name")
    primaryContactLastName = models.CharField(max_length=100, blank=True, null=True, default=None, verbose_name="Primary contact's last name")
    businessAddressLine1 = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Business Address Line 1")
    businessAddressLine2 = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Business Address Line 2")
    businessAddressCity = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Business Address City")
    businessAddressState = models.ForeignKey(PoliticalRegion, on_delete=models.SET_NULL, blank=True, null=True, default=None, verbose_name="Business Address State")
    businessAddressZipCode = models.CharField(max_length=25, blank=True, null=True, default=None, verbose_name="Business Address Zip Code")

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name,
            'phone': self.phone.as_national if self.phone else None,
            'email': self.email,
            'websiteAddress': self.websiteAddress,
            'fax': self.fax.as_national if self.fax else None,
            'primaryContactFirstName': self.primaryContactFirstName,
            'primaryContactLastName': self.primaryContactLastName,
            'businessAddressLine1': self.businessAddressLine1,
            'businessAddressLine2': self.businessAddressLine2,
            'businessAddressCity': self.businessAddressCity,
            'businessAddressState': self.businessAddressState.to_dict() if self.businessAddressState else None,
            'businessAddressZipCode': self.businessAddressZipCode
        }

    class Meta:
        ordering = ('name',)

class Identity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.pk,
            'name': self.name,
            'description': self.description
        }

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "identities"

class ProductionPractice(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, default=None)
    definitionLink = models.URLField(max_length=255, null=True, blank=True, default=None, help_text="If an official definition is online, copy the URL here.")

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'definitionLink': self.definitionLink
        }

    class Meta:
        ordering = ('name',)

class Provider(models.Model):
    TERNARY_YES_NO_CHOICES = (
        ('Unknown', 'Unknown'),
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    name = models.CharField(max_length=255, verbose_name="Supplier Name")
    outreachConductor = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name='Outreach conducted by', help_text="The name of the teammate who reached out to this supplier")
    dateInfoAdded = models.DateTimeField(auto_now_add=True, verbose_name='Record created date')
    dateInfoUpdated = models.DateTimeField(auto_now=True, verbose_name='Date information updated', help_text="This is automatic.")
    soldToSchoolsBefore = models.CharField(max_length=20, choices=TERNARY_YES_NO_CHOICES, default='Unknown', verbose_name='This supplier has sold to schools before')
    description = models.TextField(blank=True, null=True, default=None, verbose_name="Brief Description", help_text="2-3 Sentences")
    primaryContactFirstName = models.CharField(max_length=100, blank=True, null=True, default=None, verbose_name="Primary contact's first name")
    primaryContactLastName = models.CharField(max_length=100, blank=True, null=True, default=None, verbose_name="Primary contact's last name")
    businessAddressLine1 = models.CharField(max_length=255, verbose_name="Business Address Line 1", blank=True, null=True, default=None)
    businessAddressLine2 = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Business Address Line 2")
    businessAddressCity = models.CharField(max_length=255, verbose_name="Business Address City")
    businessAddressState = models.ForeignKey(PoliticalRegion, on_delete=models.PROTECT, verbose_name="Business Address State", related_name="providerBusinessAddresses")
    businessAddressZipCode = models.CharField(max_length=25, verbose_name="Business Address Zip Code", blank=True, null=True, default=None)

    physicalAddressIsSame = models.BooleanField(default=False, verbose_name="Physical address is the same as business address")

    physicalAddressLine1 = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Physical Address Line 1")
    physicalAddressLine2 = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Physical Address Line 2")
    physicalAddressCity = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Physical Address City")
    physicalAddressState = models.ForeignKey(PoliticalRegion, on_delete=models.SET_NULL, blank=True, null=True, default=None, verbose_name="Physical Address State", related_name="providerPhysicalAddresses")
    physicalAddressZipCode = models.CharField(max_length=25, blank=True, null=True, default=None, verbose_name="Physical Address Zip Code")

    officePhone = PhoneNumberField(verbose_name="Office Phone", blank=True, null=True, default=None)
    cellPhone = PhoneNumberField(blank=True, null=True, default=None, verbose_name="Cell Phone")
    email = models.EmailField(max_length=255, null=True, blank=True, default=None)
    websiteAddress = models.URLField(max_length=255, null=True, blank=True, default=None, verbose_name="Website Address", help_text="Try to include either http:// (good) or https:// (better if available)")

    identities = models.ManyToManyField(Identity, blank=True)

    notes = models.TextField(null=True, blank=True, default=None, verbose_name="Additional Notes")

    #######################################################################
    #   The following may need to be "Provider-Product Specific"
    #######################################################################

    productLiabilityInsurance = models.CharField(max_length=20, choices=TERNARY_YES_NO_CHOICES, default='Unknown', verbose_name='This supplier has product liability insurance')
    productLiabilityInsuranceAmount = MoneyField(max_digits=10, decimal_places=0, default_currency='USD', null=True, blank=True, default=None, verbose_name="Product Liability Insurance Amount")
    deliveryMethods = models.ManyToManyField(DeliveryMethod, blank=True, verbose_name='Delivery Methods')
    regionalAvailability = models.ManyToManyField(PoliticalSubregion, blank=True, verbose_name='Regions where product is available')
    orderMinimum = MoneyField(max_digits=8, decimal_places=2, default_currency='USD', null=True, blank=True, default=None, verbose_name='Order Minimum')
    deliveryMinimum = MoneyField(max_digits=8, decimal_places=2, default_currency='USD', null=True, blank=True, default=None, verbose_name='Delivery Minimum')
    distributors = models.ManyToManyField(Distributor, blank=True)
    productionPractices = models.ManyToManyField(ProductionPractice, blank=True, verbose_name='Production Practices')

    class Meta:
        verbose_name="supplier"
        verbose_name_plural="suppliers"
        ordering = ('name', 'dateInfoUpdated',)

    @property
    def components_offered(self):
        component_ids = []
        for product in self.providerproduct_set.all():
            for component in product.category.usdaComponentCategories.all():
                if component.id not in component_ids:
                    component_ids.append(component.id)
        return ComponentCategory.objects.filter(id__in=component_ids)


    def to_json(self):
        products = [x.to_json() for x in self.providerproduct_set.all()]
        product_categories =[]
        for product in self.providerproduct_set.all():
            product_ancestor_category = product.category.get_prime_ancestor().to_json()
            is_dupe = False
            for category in product_categories:
                if product_ancestor_category == category:
                    is_dupe = True
            if not is_dupe:
                product_categories.append(product_ancestor_category)
        return {
            'id': self.id,
            'pk': self.pk,
            'name': self.name,
            'outreachConductor': self.outreachConductor,
            'dateInfoAdded': self.dateInfoAdded.strftime('%D'),
            'dateInfoUpdated': self.dateInfoUpdated.strftime('%D'),
            'soldToSchoolsBefore': self.soldToSchoolsBefore,
            'description': self.description,
            'primaryContactFirstName': self.primaryContactFirstName,
            'primaryContactLastName': self.primaryContactLastName,
            'businessAddressLine1': self.businessAddressLine1,
            'businessAddressLine2': self.businessAddressLine2,
            'businessAddressCity': self.businessAddressCity,
            'businessAddressState': self.businessAddressState.to_dict() if self.businessAddressState else None,
            'businessAddressZipCode': self.businessAddressZipCode,
            'physicalAddressIsSame': self.physicalAddressIsSame,
            'physicalAddressLine1': self.physicalAddressLine1,
            'physicalAddressLine2': self.physicalAddressLine2,
            'physicalAddressCity': self.physicalAddressCity,
            'physicalAddressState': self.physicalAddressState.to_dict() if self.physicalAddressState else None,
            'physicalAddressZipCode': self.physicalAddressZipCode,
            'officePhone': self.officePhone.as_national if self.officePhone else None,
            'cellPhone': self.cellPhone.as_national if self.cellPhone else None,
            'email': self.email,
            'websiteAddress': self.websiteAddress,
            'identities': [x.to_dict() for x in self.identities.all()],
            'notes': self.notes,
            #######################################################################
            #   The following may need to be "Provider-Product Specific"
            #######################################################################
            'productLiabilityInsurance': self.productLiabilityInsurance,
            'productLiabilityInsuranceAmount': str(self.productLiabilityInsuranceAmount) if (self.productLiabilityInsuranceAmount and not self.productLiabilityInsuranceAmount == None) else None,
            'deliveryMethods': [{'id': x.id, 'name': x.name} for x in self.deliveryMethods.all()],
            'regionalAvailability': [{'id': x.id, 'name': x.name} for x in self.regionalAvailability.all()],
            'orderMinimum': str(self.orderMinimum),
            'deliveryMinimum': str(self.deliveryMinimum),
            'distributors': [{'id': x.id, 'name': x.name} for x in self.distributors.all()],
            'productionPractices': [{'id': x.id, 'name': x.name} for x in self.productionPractices.all()],
            'products': products,
            'product_categories': product_categories,
        }

    def to_dict(self):
        product_categories =[]
        for product in self.providerproduct_set.all():
            product_ancestor_category = product.category.get_prime_ancestor()
            if not product_ancestor_category in product_categories:
                product_categories.append(product_ancestor_category)

        out_dict = self.to_json()
        out_dict['dateInfoAdded'] = self.dateInfoAdded
        out_dict['dateInfoUpdated'] = self.dateInfoUpdated
        out_dict['businessAddressState'] = self.businessAddressState
        out_dict['physicalAddressState'] = self.physicalAddressState
        out_dict['identities'] = self.identities
        out_dict['productLiabilityInsuranceAmount'] = self.productLiabilityInsuranceAmount
        out_dict['deliveryMethods'] = self.deliveryMethods
        out_dict['regionalAvailability'] = self.regionalAvailability
        out_dict['orderMinimum'] = self.orderMinimum
        out_dict['deliveryMinimum'] = self.deliveryMinimum
        out_dict['distributors'] = self.distributors
        out_dict['productionPractices'] = self.productionPractices
        out_dict['products'] = self.providerproduct_set.all()
        out_dict['product_categories'] = product_categories
        return out_dict

    def __str__(self):
        return self.name

class CapacityMeasurement(models.Model):
    TYPE_CHOICES = (
        ('Area', 'Area'),
        ('Count', 'Count'),
        ('Volume', 'Volume'),
        ('Weight', 'Weight'),
    )
    measurementType = models.CharField(max_length=20, choices=TYPE_CHOICES)
    unit = models.CharField(max_length=100, help_text="Like 'lbs' for weight, 'acres' for area, or 'head' for count")
    # filterQuestion = models.CharField(max_length=255, help_text="Like 'Providers with at least '")
    # Code filter question to be "Providers with at least |_____| {{ measurement.unit }}."

    def __str__(self):
        return self.unit

    def to_dict(self):
        return {
            'id': self.id,
            'measurementType': self.measurementType,
            'unit': self.unit
        }

    class Meta:
        ordering = ('measurementType', 'unit')

class ComponentCategory(models.Model):
    name = models.CharField(max_length=150)
    order = models.IntegerField(default=9)
    description = models.TextField(null=True, blank=True, default=None)
    imageFile = models.ImageField(null=True, blank=True, default=None, help_text="Upload a file if one is available (preferred)")
    imageLink = models.URLField(max_length=1000, null=True, blank=True, default=None, help_text="Link to viable online image, used if no imageFile is provided")
    imageAttribution = models.TextField(null=True, blank=True, default=None)
    usdaLink = models.URLField(max_length=255, null=True, blank=True, default=None, help_text="A link to the USDA Food Buying Guide information for this Component Category")

    def __str__(self):
        return self.name

    @property
    def image(self):
        if self.imageFile:
            return '/media/%s' % str(self.image)
        return self.imageLink


    class Meta:
        verbose_name_plural = "USDA component categories"
        ordering = ('order', 'name',)

class CategoryManager(models.QuerySet):
    # we need to trigger 'saves' on all decendants to reset 'full_name' values
    def delete(self, *args, **kwargs):
        impacted_children = []
        for category in self:
            impacted_children += [x.pk for x in category.get_children()]
        super(CategoryManager, self).delete(*args, **kwargs)
        children = ProductCategory.objects.filter(pk__in=impacted_children)
        for child in children:
            child.save()

class ProductCategory(models.Model):
    objects = CategoryManager.as_manager()
    name = models.CharField(max_length=100)
    capacityMeasurement = models.ForeignKey(CapacityMeasurement, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, default=None)
    image = models.ImageField(null=True, blank=True, default=None, upload_to='category_images')
    full_name = models.TextField(null=True, blank=True, default=None)
    usdaComponentCategories = models.ManyToManyField(ComponentCategory, blank=True, verbose_name='USDA Component Categories')
    # ancestor_count = models.IntegerField(default=0)

    @property
    def componentCategories(self):
        if not self.usdaComponentCategories.all().count() > 0:
            if self.parent:
                return self.parent.componentCategories
        return self.usdaComponentCategories.all()

    @property
    def image_string(self):
        if not self.image:
            if not self.parent:
                image = settings.DEFAULT_CATEGORY_IMAGE
            else:
                image = self.parent.image_string
        else:
            image = '/media/%s' % str(self.image)
        return image

    def to_dict(self):
        return {
            'id': self.id,
            'pk': self.pk,
            'name': self.name,
            'capacityMeasurement': self.capacityMeasurement.to_dict() if self.capacityMeasurement else None,
            'parent': self.parent.to_dict() if self.parent else None,
            'image': self.image_string,
            'usdaComponentCategories': self.componentCategories,
        }

    def to_json(self):
        return {
            'id': self.id,
            'pk': self.pk,
            'name': self.name,
            'capacityMeasurement': self.capacityMeasurement.to_dict() if self.capacityMeasurement else None,
            'parent': {'id': self.parent.id, 'name': self.parent.name} if self.parent else None,
            'image': self.image_string,
            'usdaComponentCategories': [{'id': x.id, 'name': x.name, 'order': x.order} for x in self.componentCategories],
        }

    def __str__(self):
        if self.parent:
            return "%s > %s" % (str(self.parent), self.name)
        else:
            return self.name

    def get_children(self):
        children = ProductCategory.objects.filter(parent=self)
        return children

    def get_decendants(self):
        children = self.get_children()
        decendants_list = [x for x in children]
        for child in children:
            decendants_list = decendants_list + child.get_decendants()
        return decendants_list

    def get_products(self):
        # TODO: Cache this!
        decendants = self.get_decendants()
        decendants.append(self)
        category_products = Product.objects.filter(category__in=decendants)
        return category_products

    def get_provider_products(self):
        # TODO: Cache this!
        decendants = self.get_decendants()
        decendants.append(self)
        category_provider_products = ProviderProduct.objects.filter(category__in=decendants)
        return category_provider_products

    def get_providers(self):
        products = self.get_provider_products()
        provider_ids = list(set([x.provider.pk for x in products]))
        providers = Provider.objects.filter(pk__in=provider_ids)
        return providers

    def get_ancestors(self):
        if self.parent:
            return self.parent.get_ancestors() + [self.parent]
        else:
            return []

    def get_ancestor_count(self):
        ancestors = self.get_ancestors()
        return len(ancestors)

    def get_prime_ancestor(self):
        if self.parent:
            return self.parent.get_prime_ancestor()
        else:
            return self

    # TODO: Clear caches on save for this and parents.
    def save(self, *args, **kwargs):
        # self.ancestor_count = self.get_ancestor_count()
        # super(ProductCategory, self).save(*args, **kwargs)
        self.full_name = str(self)
        super(ProductCategory, self).save(*args, **kwargs)
        children = self.get_children()
        for child in children:
            child.save()

    def delete(self, *args, **kwargs):
        # we need to trigger 'saves' on all decendants to reset 'full_name' values
        impacted_children = [x.pk for x in self.get_children()]
        super(ProductCategory, self).delete(*args, **kwargs)
        children = ProductCategory.objects.filter(pk__in=impacted_children)
        for child in children:
            child.save()

    class Meta:
        verbose_name_plural = "product categories"
        ordering = ('full_name',)

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    image = models.ImageField(null=True, blank=True, default=None, upload_to='product_images')
    description = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class ProviderProduct(models.Model):
    TERNARY_YES_NO_CHOICES = (
        ('Unknown', 'Unknown'),
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Product Name")
    dateInfoAdded = models.DateTimeField(auto_now_add=True, verbose_name='Record created date')
    dateInfoUpdated = models.DateTimeField(auto_now=True, verbose_name='Date information updated', help_text="This is automatic.")
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, verbose_name="Product Category")
    image = models.ImageField(null=True, blank=True, default=None, upload_to='product_images')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    capacityValue = models.IntegerField(null=True, blank=True, default=None, verbose_name="Capacity (value)")
    capacityMeasurement = models.ForeignKey(CapacityMeasurement, null=True, blank=True, default=None, on_delete=models.SET_NULL, verbose_name="Capacity (Measurement)")
    description = models.TextField(null=True, blank=True, default=None, help_text="Discription shown in search view", verbose_name="Product Description")
    notes = models.TextField(null=True, blank=True, default=None, verbose_name="Additional Notes")

    #######################################################################
    #   The following may need to be "Provider Specific"
    #######################################################################

    productLiabilityInsurance = models.CharField(max_length=20, choices=TERNARY_YES_NO_CHOICES, default='Unknown', verbose_name='Has insurance')
    productLiabilityInsuranceAmount = MoneyField(max_digits=10, decimal_places=0, default_currency='USD', null=True, blank=True, default=None, verbose_name="Product liability Insurance amount")
    deliveryMethods = models.ManyToManyField(DeliveryMethod, blank=True, verbose_name="Delivery Methods for this product")
    regionalAvailability = models.ManyToManyField(PoliticalSubregion, blank=True, verbose_name="Regions where this product is available")
    orderMinimum = MoneyField(max_digits=8, decimal_places=2, default_currency='USD', null=True, blank=True, default=None, verbose_name="Order Minimum")
    deliveryMinimum = MoneyField(max_digits=8, decimal_places=2, default_currency='USD', null=True, blank=True, default=None, verbose_name="Delivery Minimum")
    distributors = models.ManyToManyField(Distributor, blank=True)
    productionPractices = models.ManyToManyField(ProductionPractice, blank=True, verbose_name="Production Practices")

    def __str__(self):
        return "%s: %s - %s" % (self.name, str(self.category), str(self.provider))

    def to_dict(self):
        out_dict = self.to_json()
        out_dict['category'] = self.category
        out_dict['provider'] = self.provider
        out_dict['productLiabilityInsuranceAmount'] = self.productLiabilityInsuranceAmount
        out_dict['deliveryMethods'] = self.deliveryMethods
        out_dict['regionalAvailability'] = self.regionalAvailability
        out_dict['orderMinimum'] = self.orderMinimum
        out_dict['deliveryMinimum'] = self.deliveryMinimum
        out_dict['distributors'] = self.distributors
        out_dict['productionPractices'] = self.productionPractices
        out_dict['capacityMeasurement'] = self.capacityMeasurement
        out_dict['dateInfoUpdated'] = self.dateInfoUpdated
        return out_dict

    @property
    def image_string(self):
        if not self.image:
            if not self.category:
                image = settings.DEFAULT_CATEGORY_IMAGE
            else:
                image = self.category.to_json()['image']
        else:
            image = '/media/%s' % str(self.image)
        return image

    def to_json(self):
        return {
            'id': self.pk,
            'pk': self.pk,
            'name': self.name,
            'category': self.category.to_json() if self.category else None,
            'image': self.image_string,
            'provider': {'name':self.provider.name, 'id': self.provider.id, 'pk': self.provider.pk} if self.provider else {'name':None, 'id': None},
            'description': self.description,
            'notes': self.notes,
            'productLiabilityInsurance': self.productLiabilityInsurance,
            'productLiabilityInsuranceAmount': str(self.productLiabilityInsuranceAmount),
            'deliveryMethods': [{'id': x.id, 'name': x.name} for x in self.deliveryMethods.all()],
            'regionalAvailability': [{'id': x.id, 'name': x.name} for x in self.regionalAvailability.all()],
            'orderMinimum': str(self.orderMinimum),
            'deliveryMinimum': str(self.deliveryMinimum),
            'distributors': [{'id': x.id, 'name': x.name} for x in self.distributors.all()],
            'productionPractices': [{'id': x.id, 'name': x.name} for x in self.productionPractices.all()],
            'capacityValue': self.capacityValue,
            'capacityMeasurement': self.capacityMeasurement.to_dict() if self.capacityMeasurement else None,
            'dateInfoUpdated': self.dateInfoUpdated.strftime('%D'),
        }

    class Meta:
        verbose_name = 'supplier product'
        verbose_name_plural = 'supplier products'
        ordering = ('category', 'provider')
