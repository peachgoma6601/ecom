from django.urls import path
from .views import store,product_detail
urlpatterns =   [
    path('',store,name='store'),
    path('<slug:catagory_slug>',store,name='products_by_catagory'),
    path('<slug:catagory_slug>/<slug:product_slug>',product_detail,name='product_detail'),
]