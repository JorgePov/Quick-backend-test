from django.urls import path
from .views import BillByIdView, BillView, BillProductView, BillProductByIdView

urlpatterns = [
    path('bills', BillView.as_view()),
    path('bills/<int:pk>', BillByIdView.as_view()),
    
    path('bills/products/', BillProductView.as_view()),
    path('bills/<int:id_bills>/products/<int:id_products>', BillProductByIdView.as_view()),
    
]
