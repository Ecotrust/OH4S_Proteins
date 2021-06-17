# Generated by Django 3.2 on 2021-06-15 18:23

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0008_alter_contentpage_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentpage',
            name='content',
            field=wagtail.core.fields.StreamField([('image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.core.blocks.RichTextBlock(blank=True, features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'superscript', 'subscript', 'strikethrough', 'blockquote', 'image', 'embed', 'code'])), ('google_form', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.URLBlock())], help_text='The URL for the Google form. This will be loaded into a popup when clicked.', label='Google Form Link', template='cms/google_form.html')), ('HTML', wagtail.core.blocks.RawHTMLBlock(help_text='For fine-tuning very specific/custom blocks.', label='Custom HTML')), ('Embedded_Media', wagtail.embeds.blocks.EmbedBlock(label='Embedded Media'))]),
        ),
        migrations.AlterField(
            model_name='footerpage',
            name='column_1',
            field=wagtail.core.fields.StreamField([('image', wagtail.images.blocks.ImageChooserBlock()), ('externalLink', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.URLBlock())], label='External Link')), ('internalLink', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.PageChooserBlock())], label='Internal Link')), ('google_form', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.URLBlock())], help_text='The URL for the Google form. This will be loaded into a popup when clicked.', label='Google Form Link', template='cms/google_form_footer.html')), ('text', wagtail.core.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'superscript', 'subscript', 'strikethrough', 'blockquote', 'image', 'embed', 'code']))]),
        ),
        migrations.AlterField(
            model_name='footerpage',
            name='column_2',
            field=wagtail.core.fields.StreamField([('image', wagtail.images.blocks.ImageChooserBlock()), ('externalLink', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.URLBlock())], label='External Link')), ('internalLink', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.PageChooserBlock())], label='Internal Link')), ('google_form', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.URLBlock())], help_text='The URL for the Google form. This will be loaded into a popup when clicked.', label='Google Form Link', template='cms/google_form_footer.html')), ('text', wagtail.core.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'superscript', 'subscript', 'strikethrough', 'blockquote', 'image', 'embed', 'code']))]),
        ),
        migrations.AlterField(
            model_name='footerpage',
            name='column_3',
            field=wagtail.core.fields.StreamField([('image', wagtail.images.blocks.ImageChooserBlock()), ('externalLink', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.URLBlock())], label='External Link')), ('internalLink', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.PageChooserBlock())], label='Internal Link')), ('google_form', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock()), ('link', wagtail.core.blocks.URLBlock())], help_text='The URL for the Google form. This will be loaded into a popup when clicked.', label='Google Form Link', template='cms/google_form_footer.html')), ('text', wagtail.core.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'superscript', 'subscript', 'strikethrough', 'blockquote', 'image', 'embed', 'code']))]),
        ),
    ]