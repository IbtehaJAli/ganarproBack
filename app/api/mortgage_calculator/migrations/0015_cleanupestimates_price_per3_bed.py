# Generated by Django 4.0.4 on 2023-01-21 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mortgage_calculator', '0014_alter_cleanupestimates_no_stories'),
    ]

    operations = [
        migrations.AddField(
            model_name='cleanupestimates',
            name='price_per3_bed',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
