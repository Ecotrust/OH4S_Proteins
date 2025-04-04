# Generated by Django 3.2 on 2021-06-15 18:23

from django.db import migrations
import wagtail.blocks
import wagtail.fields
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
            field=wagtail.fields.StreamField([('image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.blocks.RichTextBlock(blank=True, features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'superscript', 'subscript', 'strikethrough', 'blockquote', 'image', 'embed', 'code'])), ('google_form', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.URLBlock())], help_text='The URL for the Google form. This will be loaded into a popup when clicked.', label='Google Form Link', template='cms/google_form.html')), ('HTML', wagtail.blocks.RawHTMLBlock(help_text='For fine-tuning very specific/custom blocks.', label='Custom HTML')), ('Embedded_Media', wagtail.embeds.blocks.EmbedBlock(label='Embedded Media'))]),
        ),
        migrations.AlterField(
            model_name='footerpage',
            name='column_1',
            field=wagtail.fields.StreamField([('image', wagtail.images.blocks.ImageChooserBlock()), ('externalLink', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.URLBlock())], label='External Link')), ('internalLink', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.PageChooserBlock())], label='Internal Link')), ('google_form', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.URLBlock())], help_text='The URL for the Google form. This will be loaded into a popup when clicked.', label='Google Form Link', template='cms/google_form_footer.html')), ('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'superscript', 'subscript', 'strikethrough', 'blockquote', 'image', 'embed', 'code']))]),
        ),
        migrations.AlterField(
            model_name='footerpage',
            name='column_2',
            field=wagtail.fields.StreamField([('image', wagtail.images.blocks.ImageChooserBlock()), ('externalLink', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.URLBlock())], label='External Link')), ('internalLink', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.PageChooserBlock())], label='Internal Link')), ('google_form', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.URLBlock())], help_text='The URL for the Google form. This will be loaded into a popup when clicked.', label='Google Form Link', template='cms/google_form_footer.html')), ('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'superscript', 'subscript', 'strikethrough', 'blockquote', 'image', 'embed', 'code']))]),
        ),
        migrations.AlterField(
            model_name='footerpage',
            name='column_3',
            field=wagtail.fields.StreamField([('image', wagtail.images.blocks.ImageChooserBlock()), ('externalLink', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.URLBlock())], label='External Link')), ('internalLink', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.PageChooserBlock())], label='Internal Link')), ('google_form', wagtail.blocks.StructBlock([('text', wagtail.blocks.CharBlock()), ('link', wagtail.blocks.URLBlock())], help_text='The URL for the Google form. This will be loaded into a popup when clicked.', label='Google Form Link', template='cms/google_form_footer.html')), ('text', wagtail.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'superscript', 'subscript', 'strikethrough', 'blockquote', 'image', 'embed', 'code']))]),
        ),
    ]
