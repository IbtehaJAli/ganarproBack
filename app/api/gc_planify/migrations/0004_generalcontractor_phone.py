# Generated by Django 4.0.4 on 2023-09-07 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gc_planify', '0003_generalcontractor_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalcontractor',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
