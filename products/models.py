from django.db import models
from django.db.models import Manager

class ProductManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Product(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    objects = ProductManager()

    def __str__(self):
        return f"{self.name} - {self.description}"
