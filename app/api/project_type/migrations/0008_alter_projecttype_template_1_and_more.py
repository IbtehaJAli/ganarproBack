# Generated by Django 4.0.4 on 2023-06-15 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_type', '0007_rename_temaplate_1_projecttype_template_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttype',
            name='template_1',
            field=models.FileField(blank=True, null=True, upload_to='project_type_upload/'),
        ),
        migrations.AlterField(
            model_name='projecttype',
            name='template_2',
            field=models.FileField(blank=True, null=True, upload_to='project_type_upload/'),
        ),
    ]
