# Generated by Django 5.0.6 on 2024-09-06 11:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("individual", "0010_alter_userprofile_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="receivedprofile",
            name="shared_from_username",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]