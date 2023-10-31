# Generated by Django 4.0.4 on 2023-09-07 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [

    ]

    operations = [
        migrations.CreateModel(
            name='GeneralContractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, null=True)),
                ('working_region', models.JSONField(max_length=100, null=True)),
                ('pre_qualification_url', models.URLField(max_length=50, null=True)),
                ('plan_room_url', models.URLField(max_length=50, null=True)),
                ('website', models.URLField(max_length=50, null=True)),
                ('linkedin', models.URLField(max_length=50, null=True)),
                ('facebook', models.URLField(max_length=50, null=True)),
                ('twitter', models.URLField(max_length=50, null=True)),
                ('instagram', models.URLField(max_length=50, null=True)),
                ('youtube', models.URLField(max_length=50, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='general_contractors', to='djstripe.customer')),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='general_contractors', to='djstripe.subscription')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='general_contractor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'general_contractors',
            },
        ),
    ]