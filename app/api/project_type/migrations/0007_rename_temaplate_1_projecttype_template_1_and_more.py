# Generated by Django 4.0.4 on 2023-06-14 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_type', '0006_projecttype_temaplate_1_projecttype_temaplate_2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projecttype',
            old_name='temaplate_1',
            new_name='template_1',
        ),
        migrations.RenameField(
            model_name='projecttype',
            old_name='temaplate_2',
            new_name='template_2',
        ),
    ]
