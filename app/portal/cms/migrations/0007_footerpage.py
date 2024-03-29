# Generated by Django 3.2 on 2021-06-14 22:58

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('cms', '0006_producerpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('column_1', wagtail.fields.StreamField([('image', wagtail.images.blocks.ImageChooserBlock()), ('internal_link', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'superscript', 'subscript'])), ('external_link', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'superscript', 'subscript'])), ('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'superscript', 'subscript', 'strikethrough', 'blockquote', 'image', 'embed', 'code']))])),
                ('column_2', wagtail.fields.StreamField([('image', wagtail.images.blocks.ImageChooserBlock()), ('internal_link', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'superscript', 'subscript'])), ('external_link', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'superscript', 'subscript'])), ('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'superscript', 'subscript', 'strikethrough', 'blockquote', 'image', 'embed', 'code']))])),
                ('column_3', wagtail.fields.StreamField([('image', wagtail.images.blocks.ImageChooserBlock()), ('internal_link', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'superscript', 'subscript'])), ('external_link', wagtail.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'superscript', 'subscript'])), ('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'superscript', 'subscript', 'strikethrough', 'blockquote', 'image', 'embed', 'code']))])),
                ('footer_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
