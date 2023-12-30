from django.db import models
from clients.models import Client
from products.models import Product
from utils.utils import SoftDeleteManager


class Bill(models.Model):
    company_name = models.CharField(max_length=255)
    nit = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bills')
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def __str__(self):
        return f"{self.company_name} - {self.code}"

class BillProduct(models.Model):
    id_bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='bill_products')
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bill_products')
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def __str__(self):
        return f"{self.id_bill.company_name} - {self.id_product.name} "
