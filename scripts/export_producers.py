# export_producers.py
import csv
from datetime import date
from providers.models import Provider

#Producer name
#Zip codes
#Address
#Website
#County where biz is located
#About (helpful context)
#Top level food product could be helpful - primary food products
#Delivery
#Distributors
#Self-identifiers
#Additional notes (helpful context)
#USDA meal components (if it makes sense in export)
#No phone or email, order min, liability, sold to schools, production practices, no school districts sold to

today = str(date.today())
outfile = "/tmp/oh4s_producers_{}".format(today)


with open(outfile, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Bus. Address', 'Bus. Zip', 'Bus. County', 'Phys. Address', 'Phys. Zip', 'Phys. County', 'Website', 'Description', 'Products', 'Delivery', 'Distributors', 'Identities', 'Meal Components', 'Notes'])

    for provider in Provider.objects.all():
        name = provider.name
        bus_address = provider.get_address_string('Business')
        bus_zipcode = provider.businessAddressZipCode
        bus_county = provider.businessCounty
        phys_address = provider.get_address_string('Physical')
        phys_zipcode = provider.physicalAddressZipCode
        phys_county = provider.physicalCounty
        website = provider.websiteAddress
        description = provider.description
        products = "; ".join(list(set([x.category.get_prime_ancestor().name for x in provider.providerproduct_set.all().order_by('name')])))
        delivery = "; ".join([x.name for x in provider.deliveryMethods.all()])
        distributors = "; ".join([x.name for x in provider.distributors.all()])
        identities = "; ".join([x.name for x in provider.identities.all()])
        components = "; ".join([x.name for x in provider.components_offered])
        notes = provider.notes
        writer.writerow([name, bus_address, bus_zipcode, bus_county, phys_address, phys_zipcode, phys_county, website, description, products, delivery, distributors, identities, components, notes])

