from .serializers import BillSerializer
from bills.models import Bill
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class BillView(APIView):
    def get(self, request):
        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Registra un nuevo cliente.",
        request_body=BillSerializer,
        responses={status.HTTP_201_CREATED: openapi.Response('')},
    )
    def post(self, request):
        serializer = BillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BillByIdView(APIView):
    def get_object(self, pk):
        return Bill.objects.get(pk=pk)

    def get(self, request, pk):
        bill = self.get_object(pk)
        serializer = BillSerializer(bill)
        return Response(serializer.data)

    def patch(self, request, pk):
        bill = self.get_object(pk)
        serializer = BillSerializer(bill, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bill = self.get_object(pk)
        bill.is_deleted = True 
        bill.save()
        return Response(status=status.HTTP_204_NO_CONTENT)