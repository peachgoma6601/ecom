from django.urls import path
from .views import store,product_detail,search
urlpatterns =   [
    path('',store,name='store'),
    path('catagory/<slug:catagory_slug>',store,name='products_by_catagory'),
    path('catagory/<slug:catagory_slug>/<slug:product_slug>',product_detail,name='product_detail'),
    path('search/',search,name="search")
]