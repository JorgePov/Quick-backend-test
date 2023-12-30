from django.urls import path
from .views import ProductByIdView, ProductView

urlpatterns = [
    path('products', ProductView.as_view()),
    path('products/<int:pk>', ProductByIdView.as_view()),
    
]
