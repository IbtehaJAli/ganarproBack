# Generated by Django 4.0.4 on 2023-01-13 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mortgage_calculator', '0009_cleanupestimates_project_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cleanupestimates',
            name='emergency_pricing',
        ),
    ]