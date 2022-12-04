# Generated by Django 4.1 on 2022-12-04 10:33

from django.db import migrations, models
import taxi.models


class Migration(migrations.Migration):

    dependencies = [
        ("taxi", "0024_alter_driver_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driver",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="https://avatardriver-bucket.s3.eu-north-1.amazonaws.com/default.png",
                null=True,
                upload_to=taxi.models.driver_image_file_path,
            ),
        ),
    ]
