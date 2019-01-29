from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField

class PoliticalRegion(models.Model):
    REGION_TYPE_CHOICES = (
        ('State', 'State'),
        ('Province', 'Province'),           # British Columbia Province, CA
        ('Commonwealth', 'Commonwealth'),   # Commonwealth of Virginia
        ('District', 'District'),       # District of Columbia
        ('Territory', 'Territory'),
        ('Other', 'Other'),
    )
    initialism = models.CharField(max_length=4, primary_key=True, verbose_name="Initials", help_text="i.e. 'OR' for 'Oregon'. No periods.")
    name = models.CharField(max_length=100, verbose_name="Full Name")
    country = models.CharField(max_length=150, default='USA', help_text="Default is 'USA'")
    regionType = models.CharField(max_length=30, choices=REGION_TYPE_CHOICES, default='State', verbose_name="Type of political region")

    def __str__(self):
        if self.country.lower() == 'usa' or 'united states' in self.country.lower():
            if self.regionType == 'State':
                return "%s: %s" % (self.initialism, self.regionType, self.name, self.country)
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

class Provider(models.Model):
    TERNARY_YES_NO_CHOICES = (
        ('Unknown', 'Unknown'),
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    name = models.CharField(max_length=255)
    outreachConductor = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name='Outreach conducted by', help_text="The name of the teammate who reached out to this provider")
    dateInfoAdded = models.DateTimeField(auto_now_add=True, verbose_name='Record created date')
    dateInfoUpdated = models.DateTimeField(auto_now=True, verbose_name='Record last updated date')
    soldToSchoolsBefore = models.CharField(max_length=20, choices=TERNARY_YES_NO_CHOICES, default='Unknown', verbose_name='This provider has sold to schools before')
    description = models.TextField(blank=True, null=True, default=None)
    primaryContactFirstName = models.CharField(max_length=100, blank=True, null=True, default=None, verbose_name="Primary contact's first name")
    primaryContactLastName = models.CharField(max_length=100, blank=True, null=True, default=None, verbose_name="Primary contact's last name")
    businessAddressLine1 = models.CharField(max_length=255, verbose_name="Business Address Line 1")
    businessAddressLine2 = models.CharField(max_length=255, verbose_name="Business Address Line 2")
    businessAddressCity = models.CharField(max_length=255, verbose_name="Business Address City")
    businessAddressState = models.ForeignKey(PoliticalRegion, on_delete=models.PROTECT, verbose_name="Business Address State", related_name="providerBusinessAddresses")
    businessAddressZipCode = models.CharField(max_length=25, verbose_name="Business Address Zip Code")

    physicalAddressIsSame = models.BooleanField(default=False, verbose_name="Physical address is the same as business address above")

    physicalAddressLine1 = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Physical Address Line 1")
    physicalAddressLine2 = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Physical Address Line 2")
    physicalAddressCity = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="Physical Address City")
    physicalAddressState = models.ForeignKey(PoliticalRegion, on_delete=models.SET_NULL, blank=True, null=True, default=None, verbose_name="Physical Address State", related_name="providerPhysicalAddresses")
    physicalAddressZipCode = models.CharField(max_length=25, blank=True, null=True, default=None, verbose_name="Physical Address Zip Code")

    officePhone = PhoneNumberField(verbose_name="Office Phone")
    cellPhone = PhoneNumberField(blank=True, null=True, default=None, verbose_name="Cell Phone")
    email = models.EmailField(max_length=255, null=True, blank=True, default=None)
    websiteAddress = models.URLField(max_length=255, null=True, blank=True, default=None, help_text="Try to include either http:// (good) or https:// (better if available)")

    #######################################################################
    #   The following may need to be "Provider-Product Specific"
    #######################################################################

    productLiabilityInsurance = models.CharField(max_length=20, choices=TERNARY_YES_NO_CHOICES, default='Unknown', verbose_name='This provider has product liability insurance')
    productLiabilityInsuranceAmount = MoneyField(max_digits=10, decimal_places=0, default_currency='USD', null=True, blank=True, default=None)
    deliveryMethods = models.ManyToManyField(DeliveryMethod)
    regionalAvailability = models.ManyToManyField(PoliticalSubregion)
    orderMinimum = MoneyField(max_digits=8, decimal_places=2, default_currency='USD', null=True, blank=True, default=None)
    deliveryMinimum = MoneyField(max_digits=8, decimal_places=2, default_currency='USD', null=True, blank=True, default=None)
    distributors = models.ManyToManyField(Distributor)

    class Meta:
        verbose_name="provider"
        verbose_name_plural="providers"
        ordering = ('name', 'dateInfoUpdated',)

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

    def __str__(self):
        if self.parent:
            return "%s > %s" % (self.parent.name, self.name)
        else:
            return self.name

    def get_children(self):
        children = ProductCategory.objects.filter(parent=self)
        children_list = [x for x in children]
        for child in children:
            children_list = children_list + child.get_children()
        return children_list

    def get_products(self):
        children = self.get_children()
        children.append(self)
        child_products = Product.objects.filter(category__in=children)

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    image = models.ImageField(null=True, blank=True, default=None)
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

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    #######################################################################
    #   The following may need to be "Provider Specific"
    #######################################################################

    productLiabilityInsurance = models.CharField(max_length=20, choices=TERNARY_YES_NO_CHOICES, default='Unknown', verbose_name='This provider has product liability insurance')
    productLiabilityInsuranceAmount = MoneyField(max_digits=10, decimal_places=0, default_currency='USD', null=True, blank=True, default=None)
    deliveryMethods = models.ManyToManyField(DeliveryMethod)
    regionalAvailability = models.ManyToManyField(PoliticalSubregion)
    orderMinimum = MoneyField(max_digits=8, decimal_places=2, default_currency='USD', null=True, blank=True, default=None)
    deliveryMinimum = MoneyField(max_digits=8, decimal_places=2, default_currency='USD', null=True, blank=True, default=None)
    distributors = models.ManyToManyField(Distributor)

    def __str__(self):
        return "%s - %s" % (str(self.product), str(self.provider))

    class Meta:
        ordering = ('product', 'provider')
