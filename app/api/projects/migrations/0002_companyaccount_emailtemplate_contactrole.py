# Generated by Django 4.0.4 on 2023-02-23 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('title', models.CharField(max_length=500)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('GC', 'General Contractor'), ('PB', 'Project Board')], default='PB', max_length=2, null=True)),
                ('ordering', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19)], null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='ContactRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('contact_role_id', models.CharField(db_index=True, max_length=300, unique=True)),
                ('contact_id', models.CharField(max_length=300, null=True)),
                ('name', models.CharField(db_index=True, max_length=500, null=True)),
                ('phone', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('role', models.CharField(max_length=1000, null=True)),
                ('opportunity_id', models.CharField(max_length=100, null=True)),
                ('account_id', models.CharField(max_length=100, null=True)),
                ('account_name', models.CharField(db_index=True, max_length=100, null=True)),
                ('slug', models.SlugField(max_length=3000, null=True)),
                ('opportunityid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_roles', to='projects.opportunity')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
