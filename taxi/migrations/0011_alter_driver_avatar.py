# Generated by Django 4.1 on 2022-11-06 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taxi", "0010_driver_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driver",
            name="avatar",
            field=models.ImageField(
                blank=True, default="default.png", null=True, upload_to=""
            ),
        ),
    ]