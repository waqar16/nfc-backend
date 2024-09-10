# Generated by Django 5.0.6 on 2024-09-03 10:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0005_company_receive_marketing_emails_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="display_email",
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="employee",
            name="whatsapp",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
