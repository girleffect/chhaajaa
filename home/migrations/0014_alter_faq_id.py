# Generated by Django 3.2.11 on 2022-01-29 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_faq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
