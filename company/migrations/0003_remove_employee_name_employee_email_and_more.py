# Generated by Django 5.0.6 on 2024-07-03 05:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0002_rename_bio_company_company_description"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employee",
            name="name",
        ),
        migrations.AddField(
            model_name="employee",
            name="email",
            field=models.EmailField(default="", max_length=254),
        ),
        migrations.AddField(
            model_name="employee",
            name="first_name",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="employee",
            name="last_name",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="employee",
            name="phone",
            field=models.CharField(default="", max_length=20),
        ),
        migrations.AlterField(
            model_name="employee",
            name="position",
            field=models.CharField(default="", max_length=255),
        ),
    ]
