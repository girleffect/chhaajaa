# Generated by Django 3.2.12 on 2022-11-09 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sahi_salah', '0013_sahisalahindexpage_whatsapp_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='upcomingeventsarticle',
            old_name='whatsapp_link',
            new_name='cta_button',
        ),
    ]
