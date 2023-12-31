from rest_framework import serializers
from bills.models import Bill, BillProduct

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ('company_name','nit','code','client')


class BillProductSerializar(serializers.ModelSerializer):
    class Meta:
        model = BillProduct
        fields = ('id_bill','id_product')