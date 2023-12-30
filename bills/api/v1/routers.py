from django.urls import path
from .views import BillByIdView, BillView

urlpatterns = [
    path('bills', BillView.as_view()),
    path('bills/<int:pk>', BillByIdView.as_view()),
    
]
