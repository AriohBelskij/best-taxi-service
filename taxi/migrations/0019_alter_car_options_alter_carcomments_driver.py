# Generated by Django 4.1 on 2022-11-10 18:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("taxi", "0018_alter_car_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="car",
            options={"ordering": ["-rating__average"]},
        ),
        migrations.AlterField(
            model_name="carcomments",
            name="driver",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="author_comment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]