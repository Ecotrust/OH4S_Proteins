from django import forms

class FilterForm(forms.Form):

    def __init__(self,*args,**kwargs):
        try:
            self.base_fields['product_category'].choices = kwargs.pop('product_details')
        except Exception as e:
            pass
        try:
            self.base_fields['capacity'].label = "%s per year" % kwargs.pop('production_capacity_unit')
        except Exception as e:
            pass

        super(FilterForm,self).__init__(*args,**kwargs)

    from providers.models import DeliveryMethod, PoliticalSubregion
    deliveryMethodChoices = [(y, y) for y in ['Any'] + [str(x) for x in DeliveryMethod.objects.all().order_by('name')] ]
    availabilityChoices = [(y, y) for y in ['Anywhere'] + [str(x) for x in PoliticalSubregion.objects.all().order_by('name')] ]

    product_category = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple,
                label='...by Product Details',
                choices=[],
                required=False,
    )

    capacity = forms.IntegerField(
                label="acres per year",
                required=False,
    )

    distribution = forms.ChoiceField(
                initial="Any",
                label="Method of distribution",
                choices=deliveryMethodChoices,
                required=False,
    )

    availability = forms.ChoiceField(
                initial="Anywhere",
                label="Confirmed available in",
                choices=availabilityChoices,
                required=False,
    )
