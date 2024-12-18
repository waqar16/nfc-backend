# Generated by Django 5.0.6 on 2024-08-26 16:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Appointment",
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
                (
                    "host_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                ("attendee_email", models.TextField(blank=True, null=True)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("datetime", models.DateTimeField()),
                ("google_event_id", models.CharField(max_length=255)),
                (
                    "meeting_status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("completed", "Completed")],
                        max_length=50,
                    ),
                ),
                (
                    "attendee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attended_appointments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "host",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hosted_appointments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
