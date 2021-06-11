from django.core.management.base import BaseCommand, CommandError
from providers.models import ProductCategory, ComponentCategory

class Command(BaseCommand):
    help = 'Apply Component Category associations to some Product Categories'

    def handle(self, *args, **options):
        meat = ComponentCategory.objects.get(name__iexact='meats / meat alternates')
        fruit = ComponentCategory.objects.get(name__iexact='fruits')
        milk = ComponentCategory.objects.get(name__iexact='milk')
        veg = ComponentCategory.objects.get(name__iexact='vegetables')
        grain = ComponentCategory.objects.get(name__iexact='grains')
        other = ComponentCategory.objects.get(name__iexact='other foods')

        associations = {
            'meat': {
                'component': meat,
                'categories': [
                    'beans',
                    'beef',
                    'dairy',
                    'cheese',
                    'eggs',
                    'pork',
                    'poultry',
                    'seafood',
                ]
            },
            'fruit': {
                'component': fruit,
                'categories': [
                    'apples',
                    'blackberries',
                    'blueberries',
                    'cherries',
                    'cranberries',
                    'fuzzy kiwi',
                    'grapes',
                    'kiwi berries',
                    'marionberries',
                    'peaches',
                    'pears',
                    'raspberries',
                    'rhubarb',
                    'strawberries',
                    'watermelon',
                ]
            },
            'milk': {
                'component': milk,
                'categories': [
                    'dairy',
                    'milk',
                ]
            },
            'veg': {
                'component': veg,
                'categories': [
                    'asparagus',
                    'beans',
                    'beets',
                    'broccoli',
                    'brussels sprouts',
                    'cabbage',
                    'carrots',
                    'cauliflower',
                    'corn',
                    'cucumbers',
                    'kale',
                    # 'leeks',
                    'mushrooms',
                    'onions',
                    'parsnips',
                    'peas',
                    'peppers',
                    'potatoes',
                    'radishes',
                    'salad mix',
                    'spinach',
                    'string beans',
                    'summer squash',
                    'tomatoes',
                    'turnips',
                    'winter squash',
                ]
            },
            'grain': {
                'component': grain,
                'categories': [
                    'corn',
                    'grains',
                ]
            },
            'other': {
                'component': other,
                'categories': [
                    'whipping cream',
                ]
            },
        }

        for key in associations.keys():
            component = associations[key]['component']
            for category_name in associations[key]['categories']:
                try:
                    category = ProductCategory.objects.get(name__iexact=category_name)
                    category.usdaComponentCategories.add(component)
                except Exception as e:
                    print(e)
                    print("category_name = {}".format(category_name))
