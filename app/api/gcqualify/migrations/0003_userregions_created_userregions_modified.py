# Generated by Django 4.0.4 on 2023-02-02 14:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gcqualify', '0002_remove_userregions_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregions',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userregions',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
