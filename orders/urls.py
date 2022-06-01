from django.urls import path
from .views import place_order, payment,order_complete

urlpatterns = [
    path('place_order',place_order,name='place_order'),
    path('payment/',payment,name='payment'),
    path('order_complete/',order_complete,name='order_complete')
]