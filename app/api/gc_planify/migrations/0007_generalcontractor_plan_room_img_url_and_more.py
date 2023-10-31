# Generated by Django 4.0.4 on 2023-09-08 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gc_planify', '0006_generalcontractor_facebook_img_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalcontractor',
            name='plan_room_img_url',
            field=models.URLField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='generalcontractor',
            name='pre_qualification_img_url',
            field=models.URLField(max_length=50, null=True),
        ),
    ]
