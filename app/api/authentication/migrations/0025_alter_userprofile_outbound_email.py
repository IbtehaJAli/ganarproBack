# Generated by Django 4.0.4 on 2023-08-24 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0024_auto_20230824_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='outbound_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
