# Generated by Django 4.1 on 2022-11-05 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("taxi", "0008_alter_carcomments_car"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="carcomments",
            options={"ordering": ("-created",)},
        ),
    ]
