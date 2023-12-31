# Generated by Django 4.0.4 on 2022-08-12 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_userprofile_file_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='project_contact_1_email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='project_contact_1_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='project_contact_1_phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='proposal_point_contact_email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='proposal_point_contact_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='proposal_point_contact_phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
