# Generated by Django 5.0.6 on 2024-08-21 12:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Events",
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
                ("event_name", models.CharField(max_length=255)),
                ("event_date", models.DateField()),
                ("event_time", models.TimeField()),
                ("event_location", models.CharField(max_length=255)),
                ("event_description", models.TextField()),
                ("event_longitute", models.FloatField()),
                ("event_latitude", models.FloatField()),
                (
                    "attendees",
                    models.ManyToManyField(
                        blank=True, related_name="events", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]
