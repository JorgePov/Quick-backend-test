import csv
import threading
from .serializers import ClientResgisterSerializer, ClientSerializer
from clients.api.v1.task import generate_client_csv_export, bulk_client_csv_import
from clients.models import Client
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class LoginView(APIView):

    @swagger_auto_schema(
        operation_description="Servicio encargado de autenticar un usuario.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email del usuario'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del usuario'),
            },
            required=['email', 'password'],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'document': openapi.Schema(type=openapi.TYPE_INTEGER, description='Documento del usuario'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email del usuario'),
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Identificacion interna del usuario'),
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre completo del usuario'),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Token de actualización'),
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='Token de acceso'),
                },
            ),
            401: 'Credenciales inválidas',
        },
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'document': user.document,
                'email': user.email,
                'id': user.id,
                'name': user.get_full_name(), 
                'refresh_token': refresh_token,
                'token': access_token,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class RegisterView(APIView):

    @swagger_auto_schema(
        operation_description="Registra un nuevo cliente",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'document': openapi.Schema(type=openapi.TYPE_INTEGER, description='Documento del usuario'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email del usuario'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido del usuario'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del usuario'),
            },
            required=['document', 'email', 'first_name', 'last_name', 'password'],
        ),
        responses={status.HTTP_201_CREATED: ''}
    )
    def post(self, request):
        serializer = ClientResgisterSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class ClientView(APIView):
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Servicio encargado de listar los clientes",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'document': openapi.Schema(type=openapi.TYPE_INTEGER, description='Documento del usuario'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email del usuario'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario'),
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Identificacion interna del usuario'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido del usuario'),
                },
            ),
            404: "No clients found",
        },
    )
    def get(self, request):
        try:
            clients = Client.objects.filter(is_active=True)
            serializer = ClientSerializer(clients, many=True)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response({"error": "No clients found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ClientByIdView(APIView):

    permission_classes = [IsAuthenticated]

    
    def get_object(self, pk):
        return get_object_or_404(Client, pk=pk)

    @swagger_auto_schema(
        operation_description="Servicio encargado de listar un cliente por id",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'document': openapi.Schema(type=openapi.TYPE_INTEGER, description='Documento del usuario'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email del usuario'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario'),
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Identificacion interna del usuario'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido del usuario'),
                },
            ),
            404: "Client not found",
        },
    )
    def get(self, request, pk):
        try:
            client = self.get_object(pk)
            serializer = ClientSerializer(client)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Servicio encargado de actualizar un cliente",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'document': openapi.Schema(type=openapi.TYPE_INTEGER, description='Documento del usuario'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email del usuario'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido del usuario'),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'document': openapi.Schema(type=openapi.TYPE_INTEGER, description='Documento del usuario'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email del usuario'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario'),
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Identificacion interna del usuario'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido del usuario'),
                },
            ),
            404: "Client not found",
        },
    )
    def patch(self, request, pk):
        try:
            client = self.get_object(pk)
            serializer = ClientSerializer(client, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Servicio encargado de eliminar un cliente",
        responses={
            204: "Client deleted",
            404: "Client not found",
        },
    )
    def delete(self, request, pk):
        try:
            client = self.get_object(pk)
            client.is_deleted = True
            client.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ExportClientsCSV(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Servicio encargado de exportar los clientes en formato CSV",
        responses={
            200: "La generación de CSV está en progreso. Revisar la carpeta export",
        },
    )
    def get(self, request):
        try:
            thread = threading.Thread(target=generate_client_csv_export)
            thread.start()
            return Response({'message': 'La generación de CSV está en progreso. Revisar la carpeta export'})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BulkImportClients(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Servicio encargado de importar los clientes en formato CSV",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'csv_file': openapi.Schema(type=openapi.TYPE_FILE, description='Archivo CSV con los clientes'),
            },
            required=['csv_file'],
        ),
        responses={
            202: "La carga masiva está en proceso. Revisa carpeta imports para ver el log de errores.",
            400: "Se requiere un archivo CSV válido.",
        },
    )
    def post(self, request):
        try:
            csv_file = request.FILES.get('csv_file')
            if not csv_file or not csv_file.name.endswith('.csv'):
                return Response({'error': 'Se requiere un archivo CSV válido.'}, status=status.HTTP_400_BAD_REQUEST)
            
            file_path = 'import/clients_import.csv'
            with open(file_path, 'wb') as destination:
                for chunk in csv_file.chunks():                        
                    destination.write(chunk)

            thread = threading.Thread(target=bulk_client_csv_import)
            thread.start() 
            return Response({'message': 'La carga masiva está en proceso. Revisa carpeta imports para ver el log de errores.'}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        