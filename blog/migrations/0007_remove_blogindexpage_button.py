# Generated by Django 3.1.13 on 2021-08-30 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blogindexpage_button'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogindexpage',
            name='button',
        ),
    ]
