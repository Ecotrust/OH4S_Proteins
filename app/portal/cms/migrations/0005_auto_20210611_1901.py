# Generated by Django 3.2 on 2021-06-11 19:01

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_auto_20210611_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultspage',
            name='subtitle',
            field=models.CharField(default='Results', help_text='Page header subtitle', max_length=255),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='categories_header',
            field=models.CharField(default='Search By Product Types', help_text='Header above categories', max_length=255),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='welcome_text',
            field=wagtail.fields.RichTextField(blank=True, default='<p><b>We connect school food buyers with Oregon producers who are ready to sell to schools</b></p><p><b>Get started by searching with out new filters or by selecting the product types pictured below.</b></p>><p>Need help using the site? <a href="https://vimeo.com/352842407" target="_blank">Watch our short how-to video</a>. Have ideas about how this sitecab be improved? <a hre="http://localhost:8000/contact" target="_blank">We want to her from you</a>.¿Habla Español? <a hre="http://localhost:8000/contact" target="_blank">Contáctanos aquí</a>.</p>', verbose_name='Welcome Text'),
        ),
    ]
