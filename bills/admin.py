from django.contrib import admin
from bills.models import Bill, BillProduct

admin.site.register(Bill)
admin.site.register(BillProduct)
