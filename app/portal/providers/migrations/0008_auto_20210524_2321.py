# Generated by Django 3.2 on 2021-05-24 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0007_auto_20210521_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='businessCounty',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='providerBusinessCountyLocation', to='providers.politicalsubregion', verbose_name='Business County Location'),
        ),
        migrations.AddField(
            model_name='provider',
            name='physicalCounty',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='providerPhysicalCountyLocation', to='providers.politicalsubregion', verbose_name='Physical County Location'),
        ),
    ]
