# Generated by Django 5.0.6 on 2024-08-09 13:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0003_alter_employee_profile_pic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="company",
            name="admin_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="company",
            name="company_description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="company",
            name="company_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
