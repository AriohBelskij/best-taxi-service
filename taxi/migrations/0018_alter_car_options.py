# Generated by Django 4.1 on 2022-11-10 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("taxi", "0017_alter_carcomments_text"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="car",
            options={"ordering": ["rating__average"]},
        ),
    ]
