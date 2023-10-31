# Generated by Django 4.0.4 on 2023-09-11 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gc_planify', '0007_generalcontractor_plan_room_img_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalcontractor',
            name='facebook',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='facebook_img_url',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='instagram',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='instagram_img_url',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='is_add_itbs',
            field=models.BooleanField(blank=True, default=False, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='is_davis_bacon',
            field=models.BooleanField(blank=True, default=False, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='is_public',
            field=models.BooleanField(blank=True, default=False, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='is_talent_request',
            field=models.BooleanField(blank=True, default=False, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='is_union',
            field=models.BooleanField(blank=True, default=False, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='linkedin',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='linkedin_img_url',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='plan_room_url',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='pre_qualification_img_url',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='twitter',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='twitter_img_url',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='website',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='website_img_url',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='youtube',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='generalcontractor',
            name='youtube_img_url',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
    ]
