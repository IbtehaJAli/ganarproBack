# Generated by Django 4.0.4 on 2023-07-04 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0018_alter_userprofile_customer'),
        ('projects', '0007_alter_companyaccount_market_working_region'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('region', models.CharField(max_length=10, null=True)),
                ('began_application_process', models.DateField(null=True)),
                ('confirm_on_bid_list', models.DateField(null=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plan_rooms', to='authentication.userprofile')),
                ('company_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plan_rooms', to='projects.companyaccount')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
