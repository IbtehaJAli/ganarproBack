# Generated by Django 4.0.4 on 2023-01-11 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_type', '0004_projecttype_slug'),
        ('mortgage_calculator', '0004_cleanupestimates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cleanupestimates',
            name='project_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_type_cleanup_estimates', to='project_type.projecttype'),
        ),
    ]