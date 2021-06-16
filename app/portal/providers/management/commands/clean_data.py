from django.core.management.base import BaseCommand, CommandError
from providers.models import Provider, Identity, Distributor, DeliveryMethod, ProductionPractice

class Command(BaseCommand):
    help = 'Finds duplicate records and unifies all foreign key references'

    def handle(self, *args, **options):
        family_id = Identity.objects.filter(name='Family-Owned')[0]
        for identity in Identity.objects.filter(name__icontains='family'):
            if not identity == family_id:
                for provider in identity.provider_set.all():
                    provider.identities.remove(identity)
                    provider.identities.add(family_id) # this will not duplicate family_id if already associated.
                identity.delete()

        removed_ids = []
        for prime in Identity.objects.all():
            # Looping though all identities means it will loop through
            #   identies even if they have already been deleted in this loop
            if prime.id not in removed_ids:
                dupe_list = Identity.objects.filter(name__iexact=prime.name).exclude(id=prime.id)
                for dupe in dupe_list:
                    for provider in dupe.provider_set.all():
                        provider.identities.remove(dupe)
                        provider.identities.add(prime)
                    removed_ids.append(dupe.id)
                    print("--- Removing: {dupe.name}, {dupe.id}, dupe of {prime.name}, {prime.id}".format(dupe=dupe, prime=prime))
                    dupe.delete()

        removed_ids = []
        for prime in Distributor.objects.all():
            # Looping though all distributors means it will loop through
            #   distributors even if they have already been deleted in this loop
            if prime.id not in removed_ids:
                dupe_list = Distributor.objects.filter(name__iexact=prime.name).exclude(id=prime.id)
                for dupe in dupe_list:
                    for provider in dupe.provider_set.all():
                        provider.distributors.remove(dupe)
                        provider.distributors.add(prime)
                    removed_ids.append(dupe.id)
                    print("--- Removing: {dupe.name}, {dupe.id}, dupe of {prime.name}, {prime.id}".format(dupe=dupe, prime=prime))
                    dupe.delete()

        removed_ids = []
        for prime in DeliveryMethod.objects.all():
            if prime.id not in removed_ids:
                dupe_list = DeliveryMethod.objects.filter(name__iexact=prime.name).exclude(id=prime.id)
                for dupe in dupe_list:
                    for provider in dupe.provider_set.all():
                        provider.deliveryMethods.remove(dupe)
                        provider.deliveryMethods.add(prime)
                    removed_ids.append(dupe.id)
                    print("--- Removing: {dupe.name}, {dupe.id}, dupe of {prime.name}, {prime.id}".format(dupe=dupe, prime=prime))
                    dupe.delete()

        grass_id = ProductionPractice.objects.filter(name='Grass-fed')[0]
        for practice in ProductionPractice.objects.filter(name__icontains='grass'):
            if not practice == grass_id:
                for provider in practice.provider_set.all():
                    provider.productionPractices.remove(practice)
                    provider.productionPractices.add(grass_id) # this will not duplicate grass_id if already associated.
                practice.delete()

        kosher_id = ProductionPractice.objects.filter(name='Kosher')[0]
        for practice in ProductionPractice.objects.filter(name__icontains='kosher'):
            if not practice == kosher_id:
                for provider in practice.provider_set.all():
                    provider.productionPractices.remove(practice)
                    provider.productionPractices.add(kosher_id) # this will not duplicate kosher_id if already associated.
                practice.delete()

        usda_inspected_id = ProductionPractice.objects.filter(name='USDA Inspected')[0]
        for practice in ProductionPractice.objects.filter(name__icontains='usda').filter(name__icontains='inspected'):
            if not practice == usda_inspected_id:
                for provider in practice.provider_set.all():
                    provider.productionPractices.remove(practice)
                    provider.productionPractices.add(usda_inspected_id) # this will not duplicate usda_inspected_id if already associated.
                practice.delete()

        removed_ids = []
        for prime in ProductionPractice.objects.all():
            if prime.id not in removed_ids:
                dupe_list = ProductionPractice.objects.filter(name__iexact=prime.name).exclude(id=prime.id)
                for dupe in dupe_list:
                    for provider in dupe.provider_set.all():
                        provider.productionPractices.remove(dupe)
                        provider.productionPractices.add(prime)
                    removed_ids.append(dupe.id)
                    print("--- Removing: {dupe.name}, {dupe.id}, dupe of {prime.name}, {prime.id}".format(dupe=dupe, prime=prime))
                    dupe.delete()
