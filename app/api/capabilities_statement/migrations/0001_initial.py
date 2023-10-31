# Generated by Django 4.0.4 on 2023-09-02 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='capability_statement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_name', models.CharField(max_length=50)),
                ('company_info', models.CharField(max_length=100, null=True)),
                ('company_address1', models.CharField(max_length=150, null=True)),
                ('company_address2', models.CharField(max_length=150, null=True)),
                ('owner_name', models.CharField(max_length=100, null=True)),
                ('owner_phone', models.CharField(max_length=100, null=True)),
                ('owner_email', models.CharField(max_length=100, null=True)),
                ('url', models.URLField()),
                ('about_us', models.CharField(max_length=500, null=True)),
                ('core_competencies', models.CharField(max_length=200, null=True)),
                ('core_competencies_info', models.CharField(max_length=200, null=True)),
                ('core_competencies_image', models.URLField(null=True)),
                ('past_performance', models.CharField(max_length=500, null=True)),
                ('past_performance_image', models.URLField(null=True)),
                ('difference', models.CharField(max_length=500, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='capability_statement', to='authentication.userprofile')),
            ],
        ),
    ]
