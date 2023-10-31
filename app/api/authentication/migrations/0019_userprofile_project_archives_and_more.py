# Generated by Django 4.0.4 on 2023-07-21 16:02
import django
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_delete_planroom'),
        ('authentication', '0018_alter_userprofile_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='project_archives',
            field=models.ManyToManyField(blank=True, related_name='user_project_archives', to='projects.opportunity'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='project_favorites',
            field=models.ManyToManyField(blank=True, related_name='user_project_favorites', to='projects.opportunity'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='djstripe.subscription'),
        ),
    ]
