# Generated by Django 4.0.4 on 2023-07-13 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcqualify', '0010_planroom_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregions',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
