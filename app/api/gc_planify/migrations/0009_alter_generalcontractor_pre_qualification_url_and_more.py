# Generated by Django 4.0.4 on 2023-09-11 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gc_planify', '0008_alter_generalcontractor_facebook_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalcontractor',
            name='pre_qualification_url',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='working_region',
            field=models.JSONField(blank=True, max_length=100, null=True),
        ),
    ]
