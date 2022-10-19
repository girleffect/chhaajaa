# Generated by Django 3.2.12 on 2022-10-19 19:17

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sahi_salah', '0003_sahisalahindexpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sahisalahindexpage',
            name='faqcard',
        ),
        migrations.RemoveField(
            model_name='sahisalahindexpage',
            name='testimonial',
        ),
        migrations.AddField(
            model_name='sahisalahindexpage',
            name='content',
            field=wagtail.core.fields.StreamField([('faqcard', wagtail.core.blocks.StructBlock([('faq', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Enter title', required=True)), ('description', wagtail.core.blocks.RichTextBlock(help_text='Enter description', required=False))])))])), ('testimonial', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.ListBlock(wagtail.core.blocks.CharBlock(help_text='Enter title', required=True)))]))], blank=True, null=True),
        ),
    ]
