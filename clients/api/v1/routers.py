from django.urls import path
from .views import ClientByIdView, ClientView, LoginView, RegisterView, ExportClientsCSV

urlpatterns = [
    path('auth/register', RegisterView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('clients', ClientView.as_view()),
    path('clients/<int:pk>', ClientByIdView.as_view()),
    path('clients/bills', ExportClientsCSV.as_view())
    
]
