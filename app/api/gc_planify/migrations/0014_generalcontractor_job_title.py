# Generated by Django 4.0.4 on 2023-10-06 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gc_planify', '0013_rename_email_generalcontractor_contact_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalcontractor',
            name='job_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]