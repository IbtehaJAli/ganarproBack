# Generated by Django 4.0.4 on 2023-06-16 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_type', '0009_rename_template_1_projecttype_template_a_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projecttype',
            old_name='template_A',
            new_name='template_a',
        ),
        migrations.RenameField(
            model_name='projecttype',
            old_name='template_B',
            new_name='template_b',
        ),
    ]
