# Generated by Django 4.0.4 on 2023-02-22 18:17

from django.db import migrations
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('gcqualify', '0003_userregions_created_userregions_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyaccount',
            name='id',
            field=hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='com', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='emailsubscriber',
            name='id',
            field=hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='gc_email', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userregions',
            name='id',
            field=hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=15, prefix='reg', primary_key=True, serialize=False),
        ),
    ]
