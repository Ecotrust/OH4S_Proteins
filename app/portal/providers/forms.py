from django import forms
from providers.models import DeliveryMethod, PoliticalSubregion

class FilterForm(forms.Form):

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
                choices=[],
                required=False,
    )

    availability = forms.ChoiceField(
                initial="Anywhere",
                label="Confirmed available in",
                choices=[],
                required=False,
    )

    def __init__(self,*args,**kwargs):
        try:
            product_details_choices = kwargs.pop('product_details')
        except KeyError:
            product_details_choices = None
        try:
            production_capacity_unit = kwargs.pop('production_capacity_unit')
        except KeyError:
            production_capacity_unit = None

        super(FilterForm,self).__init__(*args,**kwargs)

        if product_details_choices is not None:
            self.fields['product_category'].choices = product_details_choices
            self.fields['product_category'].initial = [x[0] for x in product_details_choices]
        if production_capacity_unit is not None:
            self.fields['capacity'].label = "%s per year" % production_capacity_unit

        self.fields['distribution'].choices = [(-1, 'Any')] + [
            (x.pk, str(x)) for x in DeliveryMethod.objects.all().order_by('name')
        ]
        self.fields['availability'].choices = [(-1, 'Anywhere')] + [
            (x.pk, str(x)) for x in PoliticalSubregion.objects.all().order_by('name')
        ]
