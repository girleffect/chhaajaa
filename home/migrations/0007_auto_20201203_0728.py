# Generated by Django 3.1.2 on 2020-12-03 07:28

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('home', '0006_auto_20201127_1136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='termpage',
            old_name='description',
            new_name='head_description',
        ),
        migrations.AddField(
            model_name='termpage',
            name='footer_description',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='termpage',
            name='footer_icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='termpage',
            name='footer_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='termpage',
            name='head_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='termpage',
            name='simplecrousal',
            field=wagtail.core.fields.StreamField([('simplecrousal', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text=' Please add crousal title here', max_length=100, required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('description', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('description', wagtail.core.blocks.CharBlock(required=False))])))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='termpage',
            name='sub_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
