# Generated by Django 4.0.4 on 2023-10-18 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_alter_opportunity_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='modified',
            field=models.DateTimeField(null=True),
        ),
    ]
