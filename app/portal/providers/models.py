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

    class Meta:
        ordering = ('name', 'region',)

class DeliveryMethod(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

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

    class Meta:
        ordering = ('name',)

class Identity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "identities"

class ProductionPractice(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, default=None)
    definitionLink = models.URLField(max_length=255, null=True, blank=True, default=None, help_text="If an official definition is online, copy the URL here.")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Provider(models.Model):
    TERNARY_YES_NO_CHOICES = (
        ('Unknown', 'Unknown'),
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    name = models.CharField(max_length=255, verbose_name="Supplier Name")
    outreachConductor = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name='Outreach conducted by', help_text="The name of the teammate who reached out to this provider")
    dateInfoAdded = models.DateTimeField(auto_now_add=True, verbose_name='Record created date')
    dateInfoUpdated = models.DateTimeField(auto_now=True, verbose_name='Date information updated', help_text="This is automatic.")
    soldToSchoolsBefore = models.CharField(max_length=20, choices=TERNARY_YES_NO_CHOICES, default='Unknown', verbose_name='This provider has sold to schools before')
    description = models.TextField(blank=True, null=True, default=None, verbose_name="Brief Description", help_text="2-3 Sentences")
    primaryContactFirstName = models.CharField(max_length=100, blank=True, null=True, default=None, verbose_name="Primary contact's first name")
    primaryContactLastName = models.CharField(max_length=100, blank=True, null=True, default=None, verbose_name="Primary contact's last name")
    businessAddressLine1 = models.CharField(max_length=255, verbose_name="Business Address Line 1")
    businessAddressLine2 = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Business Address Line 2")
    businessAddressCity = models.CharField(max_length=255, verbose_name="Business Address City")
    businessAddressState = models.ForeignKey(PoliticalRegion, on_delete=models.PROTECT, verbose_name="Business Address State", related_name="providerBusinessAddresses")
    businessAddressZipCode = models.CharField(max_length=25, verbose_name="Business Address Zip Code")

    physicalAddressIsSame = models.BooleanField(default=False, verbose_name="Physical address is the same as business address")

    physicalAddressLine1 = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Physical Address Line 1")
    physicalAddressLine2 = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Physical Address Line 2")
    physicalAddressCity = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Physical Address City")
    physicalAddressState = models.ForeignKey(PoliticalRegion, on_delete=models.SET_NULL, blank=True, null=True, default=None, verbose_name="Physical Address State", related_name="providerPhysicalAddresses")
    physicalAddressZipCode = models.CharField(max_length=25, blank=True, null=True, default=None, verbose_name="Physical Address Zip Code")

    officePhone = PhoneNumberField(verbose_name="Office Phone")
    cellPhone = PhoneNumberField(blank=True, null=True, default=None, verbose_name="Cell Phone")
    email = models.EmailField(max_length=255, null=True, blank=True, default=None)
    websiteAddress = models.URLField(max_length=255, null=True, blank=True, default=None, verbose_name="Website Address", help_text="Try to include either http:// (good) or https:// (better if available)")

    identities = models.ManyToManyField(Identity, blank=True)

    notes = models.TextField(null=True, blank=True, default=None, verbose_name="Additional Notes")

    #######################################################################
    #   The following may need to be "Provider-Product Specific"
    #######################################################################

    productLiabilityInsurance = models.CharField(max_length=20, choices=TERNARY_YES_NO_CHOICES, default='Unknown', verbose_name='This provider has product liability insurance')
    productLiabilityInsuranceAmount = MoneyField(max_digits=10, decimal_places=0, default_currency='USD', null=True, blank=True, default=None, verbose_name="Product Liability Insurance Amount")
    deliveryMethods = models.ManyToManyField(DeliveryMethod, blank=True, verbose_name='Delivery Methods')
    regionalAvailability = models.ManyToManyField(PoliticalSubregion, blank=True, verbose_name='Regions where product is available')
    orderMinimum = MoneyField(max_digits=8, decimal_places=2, default_currency='USD', null=True, blank=True, default=None, verbose_name='Order Minimum')
    deliveryMinimum = MoneyField(max_digits=8, decimal_places=2, default_currency='USD', null=True, blank=True, default=None, verbose_name='Delivery Minimum')
    distributors = models.ManyToManyField(Distributor, blank=True)
    productionPractices = models.ManyToManyField(ProductionPractice, blank=True, verbose_name='Production Practices')

    class Meta:
        verbose_name="provider"
        verbose_name_plural="providers"
        ordering = ('name', 'dateInfoUpdated',)

    def to_dict(self):
        return {
            'name': self.name,
            'outreachConductor': self.outreachConductor,
            'dateInfoAdded': self.dateInfoAdded,
            'dateInfoUpdated': self.dateInfoUpdated,
            'soldToSchoolsBefore': self.soldToSchoolsBefore,
            'description': self.description,
            'primaryContactFirstName': self.primaryContactFirstName,
            'primaryContactLastName': self.primaryContactLastName,
            'businessAddressLine1': self.businessAddressLine1,
            'businessAddressLine2': self.businessAddressLine2,
            'businessAddressCity': self.businessAddressCity,
            'businessAddressState': self.businessAddressState,
            'businessAddressZipCode': self.businessAddressZipCode,
            'physicalAddressIsSame': self.physicalAddressIsSame,
            'physicalAddressLine1': self.physicalAddressLine1,
            'physicalAddressLine2': self.physicalAddressLine2,
            'physicalAddressCity': self.physicalAddressCity,
            'physicalAddressState': self.physicalAddressState,
            'physicalAddressZipCode': self.physicalAddressZipCode,
            'officePhone': self.officePhone,
            'cellPhone': self.cellPhone,
            'email': self.email,
            'websiteAddress': self.websiteAddress,
            'identities': self.identities,
            'notes': self.notes,
            #######################################################################
            #   The following may need to be "Provider-Product Specific"
            #######################################################################
            'productLiabilityInsurance': self.productLiabilityInsurance,
            'productLiabilityInsuranceAmount': self.productLiabilityInsuranceAmount,
            'deliveryMethods': self.deliveryMethods,
            'regionalAvailability': self.regionalAvailability,
            'orderMinimum': self.orderMinimum,
            'deliveryMinimum': self.deliveryMinimum,
            'distributors': self.distributors,
            'productionPractices': self.productionPractices,
        }

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

    class Meta:
        ordering = ('measurementType', 'unit')

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    capacityMeasurement = models.ForeignKey(CapacityMeasurement, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, default=None)
    image = models.ImageField(null=True, blank=True, default=None, upload_to='category_images')
    # ancestor_count = models.IntegerField(default=0)

    def to_dict(self):
        if not self.image:
            image = settings.DEFAULT_CATEGORY_IMAGE
        else:
            image = '/media/%s' % self.image
        return {
            'pk': self.pk,
            'name': self.name,
            'capacityMeasurement': self.capacityMeasurement,
            'parent': self.parent,
            'image': image,
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

    # TODO: Clear caches on save for this and parents.
    # def save(self, *args, **kwargs):
    #     self.ancestor_count = self.get_ancestor_count()
    #     super(ProductCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "product categories"
        # ordering = ('ancestor_count', 'name')

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
        return {
            'id': self.pk,
            'name': self.name,
            'category': self.category,
            'image': self.image,
            'provider': self.provider,
            'description': self.description,
            'notes': self.notes,
            'productLiabilityInsurance': self.productLiabilityInsurance,
            'productLiabilityInsuranceAmount': self.productLiabilityInsuranceAmount,
            'deliveryMethods': self.deliveryMethods,
            'regionalAvailability': self.regionalAvailability,
            'orderMinimum': self.orderMinimum,
            'deliveryMinimum': self.deliveryMinimum,
            'distributors': self.distributors,
            'productionPractices': self.productionPractices,
            'dateInfoUpdated': self.dateInfoUpdated,
        }

    class Meta:
        ordering = ('category', 'provider')
