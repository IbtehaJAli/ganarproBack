# Generated by Django 4.0.4 on 2023-09-07 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capabilities_statement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capability_statement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capability_statement', to='authentication.userprofile'),
        ),
    ]
