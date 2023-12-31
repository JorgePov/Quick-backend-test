from .serializers import BillProductSerializar, BillSerializer
from bills.models import Bill, BillProduct
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class BillView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Obtiene todas las facturas.",
        responses={200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'company_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'nit': openapi.Schema(type=openapi.TYPE_STRING),
                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                    'client': openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )
        )}
    )
    def get(self, request):
        try:
            bills = Bill.objects.all()
            serializer = BillSerializer(bills, many=True)
            return Response(serializer.data)
        except Bill.DoesNotExist:
            return Response({"error": "No bills found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Crea una factura.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'company_name': openapi.Schema(type=openapi.TYPE_STRING),
                'nit': openapi.Schema(type=openapi.TYPE_STRING),
                'code': openapi.Schema(type=openapi.TYPE_STRING),
                'client': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['company_name', 'nit', 'code', 'client']
        ),
        responses={status.HTTP_201_CREATED: ''}
    )
    def post(self, request):
        try:
            serializer = BillSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BillByIdView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return Bill.objects.get(pk=pk)

    @swagger_auto_schema(
        operation_description="Obtiene una factura por id.",
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'company_name': openapi.Schema(type=openapi.TYPE_STRING),
                'nit': openapi.Schema(type=openapi.TYPE_STRING),
                'code': openapi.Schema(type=openapi.TYPE_STRING),
                'client': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        )}
    )
    def get(self, request, pk):
        try:
            bill = self.get_object(pk)
            serializer = BillSerializer(bill)
            return Response(serializer.data)
        except Bill.DoesNotExist:
            return Response({"error": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Actualiza una factura por id.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'company_name': openapi.Schema(type=openapi.TYPE_STRING),
                'nit': openapi.Schema(type=openapi.TYPE_STRING),
                'code': openapi.Schema(type=openapi.TYPE_STRING),
                'client': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['company_name', 'nit', 'code', 'client']
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'company_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'nit': openapi.Schema(type=openapi.TYPE_STRING),
                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                    'client': openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )
        )}
    )
    def patch(self, request, pk):
        try:
            bill = self.get_object(pk)
            serializer = BillSerializer(bill, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Bill.DoesNotExist:
            return Response({"error": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Elimina una factura por id.",
        responses={204: ''}
    )
    def delete(self, request, pk):
        try:
            bill = self.get_object(pk)
            bill.is_deleted = True 
            bill.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Bill.DoesNotExist:
            return Response({"error": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class BillProductView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Obtiene todas las facturas-producto.",
        responses={200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id_bill': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'id_product': openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )
        )}
    )
    def get(self, request):
        try:
            billProduct = BillProduct.objects.all()
            serializer = BillProductSerializar(billProduct, many=True)
            return Response(serializer.data)
        except BillProduct.DoesNotExist:
            return Response({"error": "No bills-product found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    


class BillProductByIdView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Obtiene una factura-producto por id.",
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_bill': openapi.Schema(type=openapi.TYPE_INTEGER),
                'id_product': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        )}
    )
    def get(self, request, id_bills, id_products):
        try:
            billProduct = BillProduct.objects.filter(id_bill=id_bills, id_product=id_products)
            serializer = BillProductSerializar(billProduct)
            return Response(serializer.data)
        except BillProduct.DoesNotExist:
            return Response({"error": "BillProduct not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_description="Crea una factura-producto.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_bill': openapi.Schema(type=openapi.TYPE_INTEGER),
                'id_product': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['id_bill', 'id_product']
        ),
        responses={status.HTTP_201_CREATED: '', status.HTTP_400_BAD_REQUEST: ''}
    )
    def post(self, request, id_bills, id_products):
        try:
            data = {
                'id_bill': id_bills,
                'id_product': id_products
            }
            serializer = BillProductSerializar(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
    @swagger_auto_schema(
        operation_description="Actualiza una factura-producto por id.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_bill': openapi.Schema(type=openapi.TYPE_INTEGER),
                'id_product': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['id_bill', 'id_product']
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_bill': openapi.Schema(type=openapi.TYPE_INTEGER),
                'id_product': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        )}
    ) 
    def patch(self, request, id_bills, id_products):
        try:
            billProduct = BillProduct.objects.filter(id_bill=id_bills, id_product=id_products)
            serializer = BillProductSerializar(billProduct, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Bill.DoesNotExist:
            return Response({"error": "BillProduct not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="Elimina una factura-producto por id.",
        responses={204: ''}
    )
    def delete(self, request, id_bills, id_products):
        try:
            billProduct = BillProduct.objects.filter(id_bill=id_bills, id_product=id_products)
            billProduct.is_deleted = True 
            billProduct.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Bill.DoesNotExist:
            return Response({"error": "BillProduct not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)