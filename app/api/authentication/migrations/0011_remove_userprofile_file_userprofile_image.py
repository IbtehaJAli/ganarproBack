# Generated by Django 4.0.4 on 2022-08-05 08:20

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_alter_userprofile_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='file',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
