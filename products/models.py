from django.db import models
from utils.utils import SoftDeleteManager

class Product(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def __str__(self):
        return f"{self.name} - {self.description}"
