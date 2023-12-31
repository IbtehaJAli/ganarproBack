# Generated by Django 4.0.4 on 2023-04-09 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0017_alter_userprofile_free_mode_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='profile', to='djstripe.customer'),
        ),
    ]
