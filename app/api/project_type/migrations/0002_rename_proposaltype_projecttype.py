# Generated by Django 4.0.4 on 2022-09-16 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_type', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProposalType',
            new_name='ProjectType',
        ),
    ]
