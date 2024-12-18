# Generated by Django 5.0.6 on 2024-07-19 10:59

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=255)),
                ("admin_name", models.CharField(max_length=255)),
                (
                    "company_logo",
                    models.ImageField(blank=True, null=True, upload_to="company_logo/"),
                ),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                ("address", models.TextField()),
                ("company_description", models.TextField()),
                ("website", models.URLField(blank=True, null=True)),
                ("linkedin", models.URLField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=255, null=True)),
                ("last_name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, unique=True
                    ),
                ),
                ("position", models.CharField(max_length=255)),
                ("phone", models.CharField(blank=True, max_length=15, null=True)),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("bio", models.TextField(blank=True, null=True)),
                ("facebook", models.URLField(blank=True, null=True)),
                ("instagram", models.URLField(blank=True, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                ("linkedin", models.URLField(blank=True, null=True)),
                ("github", models.URLField(blank=True, null=True)),
                ("whatsapp", models.URLField(blank=True, null=True)),
                (
                    "profile_pic",
                    models.ImageField(blank=True, null=True, upload_to="profile_pics/"),
                ),
                (
                    "registration_token",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employees",
                        to="company.company",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
