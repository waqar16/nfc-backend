# Generated by Django 5.0.6 on 2024-10-27 08:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "individual",
            "0013_rename_company_logo_receivedprofile_shared_from_company_logo_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="receivedprofile",
            name="shared_from_company_logo",
        ),
        migrations.RemoveField(
            model_name="receivedprofile",
            name="shared_from_company_name",
        ),
        migrations.RemoveField(
            model_name="receivedprofile",
            name="shared_from_first_name",
        ),
        migrations.RemoveField(
            model_name="receivedprofile",
            name="shared_from_last_name",
        ),
        migrations.RemoveField(
            model_name="receivedprofile",
            name="shared_from_position",
        ),
        migrations.RemoveField(
            model_name="receivedprofile",
            name="shared_from_profile_pic",
        ),
    ]