# Generated by Django 4.0.4 on 2023-01-13 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mortgage_calculator', '0008_cleanupestimates_bid_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='cleanupestimates',
            name='project_type',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]