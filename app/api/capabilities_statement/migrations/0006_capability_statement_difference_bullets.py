# Generated by Django 4.0.4 on 2023-09-11 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capabilities_statement', '0005_capability_statement_about_us_header_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='capability_statement',
            name='difference_bullets',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
