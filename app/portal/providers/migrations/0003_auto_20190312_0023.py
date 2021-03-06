# Generated by Django 2.1.7 on 2019-03-12 00:23

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0002_auto_20190312_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='businessAddressLine1',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Business Address Line 1'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='businessAddressZipCode',
            field=models.CharField(blank=True, default=None, max_length=25, null=True, verbose_name='Business Address Zip Code'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='officePhone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, default=None, max_length=128, null=True, verbose_name='Office Phone'),
        ),
    ]
