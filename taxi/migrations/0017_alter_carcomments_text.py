# Generated by Django 4.1 on 2022-11-09 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taxi", "0016_alter_carcomments_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carcomments",
            name="text",
            field=models.TextField(verbose_name="text"),
        ),
    ]