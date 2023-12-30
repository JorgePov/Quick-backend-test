from django.db import models
from django.db.models import Manager
from clients.models import Client

class BillManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Bill(models.Model):
    company_name = models.CharField(max_length=255)
    nit = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bills')
    is_deleted = models.BooleanField(default=False)

    objects = BillManager()

    def __str__(self):
        return f"{self.company_name} - {self.code}"
