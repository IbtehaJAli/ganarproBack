# Generated by Django 4.0.4 on 2023-02-01 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gcqualify', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregions',
            name='created',
        ),
        migrations.RemoveField(
            model_name='userregions',
            name='modified',
        ),
    ]
