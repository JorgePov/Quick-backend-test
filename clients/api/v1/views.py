from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ClientResgisterSerializer, ClientSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from clients.models import Client
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    
    @swagger_auto_schema(
        operation_description="Registra un nuevo cliente.",
        request_body=ClientResgisterSerializer,
        responses={status.HTTP_201_CREATED: openapi.Response('')},
    )
    def post(self, request):
        serializer = ClientResgisterSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ClientView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            clients = Client.objects.filter(is_active=True)
            serializer = ClientSerializer(clients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AttributeError:
            return Response({'error': 'Client attribute not found in request'}, status=status.HTTP_400_BAD_REQUEST)
        
class ClientByIdView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
