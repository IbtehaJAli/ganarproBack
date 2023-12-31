# Generated by Django 4.0.4 on 2023-02-01 12:37

from django.db import migrations, models
import hashid_field.field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyAccount',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='', primary_key=True, serialize=False)),
                ('account_id', models.CharField(db_index=True, max_length=90, unique=True)),
                ('name', models.CharField(db_index=True, max_length=500, null=True)),
                ('billing_address', models.TextField(blank=True, db_index=True, null=True)),
                ('billing_street', models.TextField(blank=True, db_index=True, null=True)),
                ('billing_city', models.CharField(blank=True, db_index=True, max_length=300, null=True)),
                ('billing_state', models.CharField(blank=True, db_index=True, max_length=300, null=True)),
                ('billing_postal_code', models.CharField(blank=True, max_length=300, null=True)),
                ('billing_country', models.CharField(blank=True, max_length=300, null=True)),
                ('phone', models.CharField(blank=True, max_length=1000, null=True)),
                ('fax', models.CharField(blank=True, max_length=1000, null=True)),
                ('website', models.CharField(blank=True, max_length=500, null=True)),
                ('industry', models.CharField(blank=True, max_length=1000, null=True)),
                ('market_working_region', models.CharField(blank=True, db_index=True, max_length=1000, null=True)),
                ('planroom_link', models.CharField(blank=True, max_length=1000, null=True)),
                ('opportunity_source', models.CharField(blank=True, max_length=1000, null=True)),
                ('opportunity_source_stage_type', models.CharField(blank=True, max_length=1000, null=True)),
                ('no_planroom_confirmed', models.CharField(blank=True, max_length=1000, null=True)),
                ('planroom_opptype', models.CharField(blank=True, max_length=1000, null=True)),
                ('no_itb_sending_confirmed', models.CharField(blank=True, max_length=1000, null=True)),
                ('twitter', models.CharField(blank=True, max_length=1000, null=True)),
                ('facebook_page', models.CharField(blank=True, max_length=1000, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=1000, null=True)),
                ('youtube', models.CharField(blank=True, max_length=1000, null=True)),
                ('prequalification_application', models.CharField(blank=True, max_length=10485760, null=True)),
                ('confirmed_no_prequal_application', models.CharField(blank=True, max_length=1000, null=True)),
                ('no_of_contacts_with_email_address', models.IntegerField(blank=True, null=True)),
                ('open_opportunities', models.IntegerField(blank=True, null=True)),
                ('signatory_to_union', models.CharField(blank=True, max_length=1000, null=True)),
                ('prevailing_wage', models.CharField(blank=True, max_length=1000, null=True)),
                ('internal_cleaning_reason', models.CharField(blank=True, max_length=1000, null=True)),
                ('enr_top_contractors_1_100', models.BooleanField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True)),
                ('slug', models.SlugField(max_length=3000)),
                ('last_modified_date', models.DateTimeField(blank=True)),
                ('status', models.CharField(blank=True, max_length=2, null=True)),
                ('multiple_offices_text', models.TextField(blank=True, null=True)),
                ('prequal_application_submit_instruction', models.TextField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
                ('logo', models.URLField(blank=True, null=True)),
                ('french_speaking', models.BooleanField(blank=True, null=True)),
                ('contact_html_email_count', models.IntegerField(blank=True, null=True)),
                ('organizational_score', models.IntegerField(blank=True, null=True)),
                ('average_project_size', models.IntegerField(blank=True, null=True)),
                ('linkedin_head_count', models.IntegerField(blank=True, null=True)),
                ('facebook_followers', models.IntegerField(blank=True, null=True)),
                ('instagram_followers', models.IntegerField(blank=True, null=True)),
                ('twitter_followers', models.IntegerField(blank=True, null=True)),
                ('youtube_subscribers', models.IntegerField(blank=True, null=True)),
                ('linked_in_followers', models.IntegerField(blank=True, null=True)),
                ('number_of_offices', models.IntegerField(blank=True, null=True)),
                ('all_opportunities', models.IntegerField(blank=True, null=True)),
                ('founded', models.CharField(blank=True, max_length=255, null=True)),
                ('naics_code', models.CharField(blank=True, max_length=255, null=True)),
                ('sic', models.CharField(blank=True, max_length=255, null=True)),
                ('top_overall_contact', models.CharField(blank=True, max_length=255, null=True)),
                ('top_estimating', models.CharField(blank=True, max_length=255, null=True)),
                ('top_project_manager', models.CharField(blank=True, max_length=255, null=True)),
                ('top_superintendent', models.CharField(blank=True, max_length=255, null=True)),
                ('top_human_resource', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter_bio', models.TextField(blank=True, null=True)),
                ('youtube_bio', models.TextField(blank=True, null=True)),
                ('facebook_bio', models.TextField(blank=True, null=True)),
                ('instagram_bio', models.TextField(blank=True, null=True)),
                ('linked_in_bio', models.TextField(blank=True, null=True)),
                ('intelconstruct_url', models.CharField(blank=True, max_length=255, null=True)),
                ('intelconstruct_company_id', models.CharField(blank=True, max_length=255, null=True)),
                ('latitude', models.CharField(blank=True, max_length=255, null=True)),
                ('longitude', models.CharField(blank=True, max_length=255, null=True)),
                ('top_c_level', models.CharField(blank=True, max_length=255, null=True)),
                ('is_archive', models.BooleanField(blank=True, default=False, verbose_name='Archive')),
                ('social_network_tier', models.CharField(blank=True, max_length=255, null=True)),
                ('organizational_tier', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmailSubscriber',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='', primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserRegions',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='', primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=40)),
                ('slug', models.CharField(db_index=True, max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
