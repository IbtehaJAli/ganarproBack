# Generated by Django 4.0.4 on 2023-08-29 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0025_alter_userprofile_outbound_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='file_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]