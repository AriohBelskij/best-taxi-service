# Generated by Django 4.1 on 2022-11-05 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("taxi", "0007_remove_carcomments_active_alter_carcomments_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carcomments",
            name="car",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments_car",
                to="taxi.car",
            ),
        ),
    ]