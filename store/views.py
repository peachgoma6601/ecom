from django.shortcuts import get_object_or_404, render
from .models import Product
from ecom1.models import Catagory
from cart.models import CartItems
from cart.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q

# Create your views here.
def store(request,catagory_slug=None):
    catagories = None 
    product = None

    if catagory_slug !=None:
        catagories =get_object_or_404(Catagory,slug=catagory_slug)
        product = Product.objects.all().filter(catagory=catagories,is_available=True)
        paginator = Paginator(product,1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = product.count()
    else:
        product = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(product,3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = product.count()
    context = {
        'product':paged_products,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)


def product_detail(request,catagory_slug,product_slug):

    try:
        single_product = Product.objects.get(catagory__slug=catagory_slug,slug=product_slug)
        in_cart = CartItems.objects.filter(product=single_product,cart__cart_id=_cart_id(request)).exists()
    except Exception as a:
        raise a

    context ={
        'single_product':single_product,
        'in_cart':in_cart

    }
    return render(request,'store/product_detail.html',context)


def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = product.count()  
    context ={
        'product':product,
        'product_count':product_count,
    }

    return render(request,'store/store.html',context)
