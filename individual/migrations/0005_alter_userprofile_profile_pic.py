# Generated by Django 5.0.6 on 2024-08-04 14:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("individual", "0004_userprofile_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="profile_pic",
            field=models.URLField(blank=True, null=True),
        ),
    ]