from django.shortcuts import render
from store.models import Product
# Create your views here.


def home(request):

    product = Product.objects.all().filter(is_available=True)

    context = {
        'product':product
    }
    return render (request,'base/home.html',context)