# Generated by Django 5.0.6 on 2024-08-19 10:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("individual", "0002_alter_receivedprofile_shared_from"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="receivedprofile",
            name="shared_from_email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name="receivedprofile",
            name="shared_from",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shared_from",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]