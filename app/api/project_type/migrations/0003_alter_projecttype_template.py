# Generated by Django 4.0.4 on 2022-09-16 16:59

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_type', '0002_rename_proposaltype_projecttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttype',
            name='template',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
