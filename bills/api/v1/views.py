from .serializers import BillSerializer
from bills.models import Bill
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class BillView(APIView):

    permission_classes = [IsAuthenticated]

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
        operation_description="Crea una nueva factura.",
        request_body=BillSerializer,
        responses={status.HTTP_201_CREATED: openapi.Response('')},
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

    def get(self, request, pk):
        try:
            bill = self.get_object(pk)
            serializer = BillSerializer(bill)
            return Response(serializer.data)
        except Bill.DoesNotExist:
            return Response({"error": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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