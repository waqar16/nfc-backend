# Generated by Django 5.0.6 on 2024-08-19 09:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("individual", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="receivedprofile",
            name="shared_from",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
