# Generated by Django 5.0.6 on 2024-08-21 09:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0002_alter_customuser_authentication_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="receive_marketing_emails",
            field=models.BooleanField(default=False),
        ),
    ]