# Generated by Django 3.1.1 on 2020-10-26 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('home', '0003_auto_20201026_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='section_about_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
