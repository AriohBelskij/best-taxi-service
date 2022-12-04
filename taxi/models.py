import os
import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
from star_ratings.models import Rating


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} {self.country}"


def driver_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.username)}-{uuid.uuid4()}{extension}"
    return "{directory}{basename}{ext}".format(directory="avatars/",
                                               basename=instance.username,
                                               ext=extension)

class Driver(AbstractUser):
    avatar = models.ImageField(null=True, blank=True,
                               default="default.png",
                               upload_to=driver_image_file_path)
    license_number = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["username"]
        verbose_name = "driver"
        verbose_name_plural = "drivers"

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.username} ({self.first_name} {self.last_name})"
        return self.username

    def get_absolute_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.pk})


class Car(models.Model):
    model = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    drivers = models.ManyToManyField(Driver, related_name="cars")
    rating = GenericRelation(Rating, related_query_name="сar_rating")

    class Meta:
        ordering = ["-rating__average"]

    def __str__(self) -> str:
        return self.model


class CarComments(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="comments_car"
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        related_name="author_comment",
    )
    text = models.TextField(verbose_name="text")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(Driver, related_name="car_comment")

    @property
    def likes_count(self) -> int:
        return self.likes.all().count()

    class Meta:
        ordering = ("-created",)

    def __str__(self) -> str:
        return f"{self.driver.username} left the comment {self.text[:10]}..."
