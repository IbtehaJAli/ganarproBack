# Generated by Django 4.0.4 on 2022-09-15 22:08

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0006_proposal_company_state_short_proposal_current_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='project_name',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
