# Generated by Django 4.1 on 2022-11-13 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("taxi", "0019_alter_car_options_alter_carcomments_driver"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="driver",
            options={
                "ordering": ["-username"],
                "verbose_name": "driver",
                "verbose_name_plural": "drivers",
            },
        ),
    ]
