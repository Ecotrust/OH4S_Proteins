# Generated by Django 3.2 on 2021-06-11 18:47

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20210527_2112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='image',
        ),
        migrations.RemoveField(
            model_name='resultspage',
            name='results_count_message',
        ),
        migrations.AddField(
            model_name='resultspage',
            name='filter_advice',
            field=wagtail.core.fields.RichTextField(blank=True, default='<p>Try removing filters to see more results</p>', help_text='Helpful advice for users confused by their results'),
        ),
        migrations.AddField(
            model_name='resultspage',
            name='results_count_message_after',
            field=models.CharField(blank=True, default='producers that meet your criteria', help_text='Text after result count', max_length=255),
        ),
        migrations.AddField(
            model_name='resultspage',
            name='results_count_message_before',
            field=models.CharField(blank=True, default='We found', help_text='Text before result count', max_length=255),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='categories_header',
            field=models.CharField(default='View  all  suppliers  for  specific  product  categories', help_text='Header above categories', max_length=255),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='filter_prompt',
            field=models.CharField(default='Search By Filtering', help_text='Language directing users to use filters', max_length=255),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='welcome',
            field=models.CharField(default='Welcome', max_length=255, verbose_name='Welcome Title'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='welcome_text',
            field=wagtail.core.fields.RichTextField(blank=True, default='<p>We connect school food buyers with Oregon producers who are ready to sell to schools. We have over 75 producers offering a wide variety of products. You can  search by product type, producer identity, location, and much more.</p><p>Need help using the site? <a href="https://vimeo.com/352842407" target="_blank">Watch our short how-to video</a> or <a href="/contact">contact us here</a>. Know a food producer who should be here? Thanks for visiting.</p>', verbose_name='Welcome Text'),
        ),
        migrations.AlterField(
            model_name='resultspage',
            name='filter_prompt',
            field=models.CharField(default='Add Filters', help_text='Language directing users to use filters', max_length=255),
        ),
    ]