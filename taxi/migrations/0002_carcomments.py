# Generated by Django 4.1 on 2022-11-03 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("taxi", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CarComments",
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
                ("body", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="taxi.car",
                    ),
                ),
                (
                    "drivers",
                    models.ManyToManyField(
                        related_name="comments", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "ordering": ("created",),
            },
        ),
    ]
