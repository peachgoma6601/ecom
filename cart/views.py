from django.shortcuts import get_object_or_404, render,redirect
from store.models import Product,ProductVariation
from .models import Cart,CartItems
from django.core.exceptions import ObjectDoesNotExist



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    product_variations = []
    if request.method == 'POST':
        for item in request.POST:
            key = item 
            value = request.POST[key]
            
            try:
                variations = ProductVariation.objects.get(product=product,variation_catagory__iexact=key,variation_value__iexact=value)
                product_variations.append(variations)

            except:
                pass



    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()


    is_cart_item_exists = CartItems.objects.filter(product=product,cart=cart).exists()

    if is_cart_item_exists:
        cart_items = CartItems.objects.filter(product=product,cart=cart)
        
        ex_var_list = []
        id = []
        for item in cart_items:
            existing_vartiations = item.product_variation.all()
            ex_var_list.append(list(existing_vartiations))
            id.append(item.id)

        if product_variations in ex_var_list:
            index = ex_var_list.index(product_variations)
            item_id = id[index]
            item = CartItems.objects.get(product=product,id=item_id)
            item.quantity +=1
            item.save()

        else:
            item = CartItems.objects.create(product=product,cart=cart)
            if len(product_variations) >0:
                item.product_variation.clear()
                item.product_variation.add(*product_variations)
            item.save()

    else:
        cart_items = CartItems.objects.create(
            product=product,
            quantity = 1 ,
            cart = cart,
        )
        if len(product_variations) >0:
            cart_items.product_variation.clear()
            for item in product_variations:
                cart_items.product_variation.add(item)
                
        cart_items.save()

    return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    try:

        cart_item = CartItems.objects.get(product=product ,cart=cart,id=cart_item_id)
        if cart_item.quantity > 1 :
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItems.objects.filter(product=product ,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request,total=0,quantity=0,cart_items=None):

    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItems.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items :
            total += (cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (2*total)/100
        grand_total = total+tax

    except ObjectDoesNotExist:
        pass 

    context ={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }

    return render(request,'store/cart.html',context)


