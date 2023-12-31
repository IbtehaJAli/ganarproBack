# Generated by Django 4.0.4 on 2023-02-28 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_hotscope'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_id', models.CharField(db_index=True, max_length=90, unique=True)),
                ('name', models.CharField(db_index=True, max_length=500, null=True)),
                ('phone', models.CharField(max_length=1000, null=True)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('title', models.CharField(db_index=True, max_length=1000, null=True)),
                ('key_estimating_project_stage_knowledge', models.BooleanField()),
                ('key_compliance', models.BooleanField()),
                ('accounting', models.BooleanField()),
                ('hiring_person', models.BooleanField()),
                ('confirmed_no_email', models.BooleanField()),
                ('no_bid_knowledge', models.BooleanField()),
                ('no_longer_employed', models.BooleanField()),
                ('created_date', models.DateTimeField(blank=True)),
                ('last_modified_date', models.DateTimeField(blank=True)),
                ('company_account_id', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=3000, null=True)),
                ('region', models.CharField(max_length=1000, null=True)),
                ('status', models.CharField(max_length=2, null=True)),
                ('html_email_count', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
            ],
        ),
    ]
