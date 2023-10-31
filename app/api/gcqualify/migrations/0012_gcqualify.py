# Generated by Django 4.0.4 on 2023-10-21 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0028_userprofile_project_viewed'),
        ('projects', '0012_alter_opportunity_modified'),
        ('gcqualify', '0011_alter_userregions_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='GcQualify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('upload', models.URLField(null=True)),
                ('note', models.TextField(null=True)),
                ('company_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gc_qualify', to='projects.companyaccount')),
                ('user_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gc_qualify', to='authentication.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
