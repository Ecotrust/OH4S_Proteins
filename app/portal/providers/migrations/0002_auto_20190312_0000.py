# Generated by Django 2.1.7 on 2019-03-12 00:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='providerproduct',
            name='dateInfoAdded',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Record created date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='providerproduct',
            name='dateInfoUpdated',
            field=models.DateTimeField(auto_now=True, help_text='This is automatic.', verbose_name='Date information updated'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='businessAddressLine2',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Business Address Line 2'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='dateInfoUpdated',
            field=models.DateTimeField(auto_now=True, help_text='This is automatic.', verbose_name='Date information updated'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='description',
            field=models.TextField(blank=True, default=None, help_text='2-3 Sentences', null=True, verbose_name='Brief Description'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Supplier Name'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='physicalAddressIsSame',
            field=models.BooleanField(default=False, verbose_name='Physical address is the same as business address'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='regionalAvailability',
            field=models.ManyToManyField(blank=True, to='providers.PoliticalSubregion', verbose_name='Regions where product is available'),
        ),
        migrations.AlterField(
            model_name='providerproduct',
            name='capacityMeasurement',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='providers.CapacityMeasurement', verbose_name='Capacity (Measurement)'),
        ),
        migrations.AlterField(
            model_name='providerproduct',
            name='capacityValue',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Capacity (value)'),
        ),
        migrations.AlterField(
            model_name='providerproduct',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='providers.ProductCategory', verbose_name='Product Category'),
        ),
        migrations.AlterField(
            model_name='providerproduct',
            name='deliveryMethods',
            field=models.ManyToManyField(blank=True, to='providers.DeliveryMethod', verbose_name='Delivery Methods for this product'),
        ),
        migrations.AlterField(
            model_name='providerproduct',
            name='deliveryMinimum',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=None, default_currency='USD', max_digits=8, null=True, verbose_name='Delivery Minimum'),
        ),
        migrations.AlterField(
            model_name='providerproduct',
            name='description',
            field=models.TextField(blank=True, default=None, help_text='Discription shown in search view', null=True, verbose_name='Product Description'),
        ),
        migrations.AlterField(
            model_name='providerproduct',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='providerproduct',
            name='orderMinimum',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=None, default_currency='USD', max_digits=8, null=True, verbose_name='Order Minimum'),
        ),
        migrations.AlterField(
            model_name='providerproduct',
            name='productLiabilityInsurance',
            field=models.CharField(choices=[('Unknown', 'Unknown'), ('Yes', 'Yes'), ('No', 'No')], default='Unknown', max_length=20, verbose_name='Has insurance'),
        ),
        migrations.AlterField(
            model_name='providerproduct',
            name='productLiabilityInsuranceAmount',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=0, default=None, default_currency='USD', max_digits=10, null=True, verbose_name='Product liability Insurance amount'),
        ),
        migrations.AlterField(
            model_name='providerproduct',
            name='productionPractices',
            field=models.ManyToManyField(blank=True, to='providers.ProductionPractice', verbose_name='Production Practices'),
        ),
        migrations.AlterField(
            model_name='providerproduct',
            name='regionalAvailability',
            field=models.ManyToManyField(blank=True, to='providers.PoliticalSubregion', verbose_name='Regions where this product is available'),
        ),
    ]
