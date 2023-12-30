from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, ClientView,ClientByIdView

urlpatterns = [
    path('auth/register', RegisterView.as_view()),
    path('auth/login', TokenObtainPairView.as_view()),
    path('clients', ClientView.as_view()),
    path('clients/<int:pk>', ClientByIdView.as_view()),
    
]
