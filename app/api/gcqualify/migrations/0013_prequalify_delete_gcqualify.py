# Generated by Django 4.0.4 on 2023-10-26 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_alter_opportunity_modified'),
        ('authentication', '0028_userprofile_project_viewed'),
        ('gcqualify', '0012_gcqualify'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreQualify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('upload', models.URLField(null=True)),
                ('note', models.TextField(null=True)),
                ('company_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pre_qualify', to='projects.companyaccount')),
                ('user_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pre_qualify', to='authentication.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='GcQualify',
        ),
    ]
