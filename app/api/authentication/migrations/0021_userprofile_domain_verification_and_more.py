# Generated by Django 4.0.4 on 2023-08-18 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0020_userprofile_customer_userprofile_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='domain_verification',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='domain_verification_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
