# Generated by Django 4.0.4 on 2023-09-14 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capabilities_statement', '0006_capability_statement_difference_bullets'),
    ]

    operations = [
        migrations.AddField(
            model_name='capability_statement',
            name='logo_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]