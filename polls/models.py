from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Product(models.Model):
    title = models.CharField(max_length=30, default="")
    owner = models.ForeignKey("polls.User", on_delete=models.CASCADE, null=True, related_name='products')
    lessons = models.ManyToManyField("polls.Lesson", related_name="products")


class Lesson(models.Model):
    title = models.CharField(max_length=30, default="")
    video_url = models.URLField(default="")
    video_duration = models.IntegerField(default=1, help_text="duration in seconds")


class LessonProgress(models.Model):
    user = models.ForeignKey("polls.User", on_delete=models.CASCADE, null=False, related_name="lessons")
    lesson = models.ForeignKey("polls.Lesson", on_delete=models.CASCADE, null=False, related_name="users_progress")
    time_viewed = models.IntegerField(help_text="duration in seconds")
    lesson_status = models.BooleanField(default=False)


class ProductAccess(models.Model):
    product = models.ForeignKey("polls.Product", on_delete=models.CASCADE, related_name='product_access')
    user = models.ForeignKey("polls.User", on_delete=models.CASCADE, related_name='access_to_products')
