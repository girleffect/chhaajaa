# Generated by Django 3.2 on 2022-10-20 18:43

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('sahi_salah', '0005_alter_sahisalahindexpage_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='sahisalahpage',
            name='content',
            field=wagtail.core.fields.StreamField([('crousalheader', wagtail.core.blocks.StructBlock([('images', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False))])))]))], blank=True, null=True),
        ),
    ]