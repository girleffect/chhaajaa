# Generated by Django 3.1.13 on 2021-09-27 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_blogindexpage_button'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='intro',
        ),
    ]
