# Generated by Django 3.2.11 on 2022-01-30 18:40

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailimages', '0023_add_choose_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='BakBakGangIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('section_1_title_1', wagtail.core.fields.RichTextField(blank=True)),
                ('section_1_card_01', models.CharField(help_text='intro of the section', max_length=200)),
                ('section_1_card_02', models.CharField(help_text='intro of the section', max_length=200)),
                ('section_1_card_03', models.CharField(help_text='intro of the section', max_length=200)),
                ('section_1_card_04', models.CharField(help_text='intro of the section', max_length=200)),
                ('section_1_title_2', models.CharField(help_text='intro of the section', max_length=200)),
                ('section_1_card_11', models.CharField(help_text='intro of the section', max_length=200)),
                ('section_1_card_12', models.CharField(help_text='intro of the section', max_length=200)),
                ('section_1_card_13', models.CharField(help_text='intro of the section', max_length=200)),
                ('section_2_title_1', wagtail.core.fields.RichTextField(blank=True)),
                ('section_2_card', wagtail.core.fields.StreamField([('testimonial', wagtail.core.blocks.StructBlock([('description', wagtail.core.blocks.RichTextBlock(required=False))]))], blank=True, null=True)),
                ('section_3_title_1', wagtail.core.fields.RichTextField(blank=True)),
                ('section_3_card', wagtail.core.fields.StreamField([('cards', wagtail.core.blocks.StructBlock([('icon', wagtail.images.blocks.ImageChooserBlock(required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False))]))], blank=True, null=True)),
                ('section_4_card', wagtail.core.fields.StreamField([('cards', wagtail.core.blocks.StructBlock([('icon', wagtail.images.blocks.ImageChooserBlock(required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False))]))], blank=True, null=True)),
                ('section_5_title', wagtail.core.fields.RichTextField(blank=True)),
                ('section_5_card_01', models.CharField(help_text='intro of the section', max_length=200)),
                ('section_5_card_02', models.CharField(help_text='intro of the section', max_length=200)),
                ('section_5_card_03', models.CharField(help_text='intro of the section', max_length=200)),
                ('section_5_card_04', models.CharField(help_text='intro of the section', max_length=200)),
                ('section_footer_title', wagtail.core.fields.RichTextField(blank=True)),
                ('section_footer_subtitle', wagtail.core.fields.RichTextField(blank=True)),
                ('header_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('section_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('section_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('section_3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('section_4', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('section_5', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('section_5_banner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('section_footer_banner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
