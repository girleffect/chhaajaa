# Generated by Django 3.1.4 on 2020-12-07 10:50

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('home', '0009_auto_20201203_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='termpage',
            name='cards',
            field=wagtail.core.fields.StreamField([('termpagecard', wagtail.core.blocks.StructBlock([('serial_number', wagtail.core.blocks.CharBlock(help_text='Add Serial Number', required=True)), ('serial_bg_color', wagtail.core.blocks.CharBlock(help_text='Add Serial Background Color in HEX value', required=True)), ('serial_text_color', wagtail.core.blocks.CharBlock(help_text='Add Serial Text Color in HEX value', required=True)), ('description', wagtail.core.blocks.RichTextBlock(help_text='Add description', required=False)), ('bg_color', wagtail.core.blocks.CharBlock(blank=True, default='#FFFFFF', help_text='Add Background Color in HEX value', null=True, required=True))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='termpage',
            name='cover_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='termpage',
            name='footer_description',
            field=wagtail.core.fields.RichTextField(blank=True, help_text='Add description', null=True),
        ),
        migrations.AddField(
            model_name='termpage',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='termpage',
            name='icon_caption',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='termpage',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='termpage',
            name='sub_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
