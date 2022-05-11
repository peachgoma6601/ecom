from django.shortcuts import get_object_or_404, render
from .models import Product
from ecom1.models import Catagory
# Create your views here.
def store(request,catagory_slug=None):
    catagories = None 
    product = None

    if catagory_slug !=None:
        catagories =get_object_or_404(Catagory,slug=catagory_slug)
        product = Product.objects.all().filter(catagory=catagories,is_available=True)
        product_count = product.count()
    else:
        product = Product.objects.all().filter(is_available=True)
        product_count = product.count()
    context = {
        'product':product,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)


def product_detail(request,catagory_slug,product_slug):

    try:
        single_product = Product.objects.get(catagory__slug=catagory_slug,slug=product_slug)
    except Exception as a:
        raise a

    context ={
        'single_product':single_product,

    }
    return render(request,'store/product_detail.html',context)