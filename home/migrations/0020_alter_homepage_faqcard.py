# Generated by Django 3.2.12 on 2022-06-15 09:47

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_alter_homepage_faqcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='faqcard',
            field=wagtail.core.fields.StreamField([('faqcard', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Enter title', required=True)), ('description', wagtail.core.blocks.RichTextBlock(help_text='Enter description', required=False))]))], blank=True, null=True),
        ),
    ]
