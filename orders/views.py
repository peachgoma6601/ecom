from django.shortcuts import redirect, render
from cart.models import CartItems
from .forms import OrderForm
from .models import Order,Payment,OrderProduct,Product
from django.views.decorators.csrf import csrf_exempt
import datetime,json
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse


def payment(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user,is_ordered=False,order_number =body['orderID'] )
    print(body)
    payment = Payment(user=request.user,payment_id=body['transID'],payment_method=body['payment_method'],amount_paid=order.order_total,status=body['status'])
    payment.save()
    order.payment=payment
    order.is_ordered = True
    order.save()
    

    cart_items = CartItems.objects.filter(user=request.user)

    for item in cart_items:

        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item =CartItems.objects.get(id=item.id)
        product_variations = cart_item.product_variation.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.product_variation.set(product_variations)
        orderproduct.save()


        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    CartItems.objects.get(user=request.user).delete()


    mail_subject = 'Thank you for order !!'
    message= render_to_string('orders/order_success_email.html',{
        'user':request.user,
        'order':order,
    })
    to_mail = request.user.email
    send_email = EmailMessage(mail_subject,message,to=[to_mail])
    send_email.send()


    data = {
        'order_number' : order.order_number,
        'transID':payment.payment_id
    }


    return JsonResponse(data)



def place_order(request,total=0,quantity=0):
    current_user = request.user

    cart_items = CartItems.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <=0 :
        return redirect('store')

    grand_total =0 
    tax = 0
    for cart_item in cart_items :
            total += (cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity
        
    tax = (2*total)/100
    grand_total = total+tax


    if request.method == 'POST':
        form = OrderForm(request.POST)
        print(form.errors)
        print(form)
        if form.is_valid():
            data = Order()
            print(data)
            print('im ok dude')
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip =request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%y'))
            mo = int(datetime.date.today().strftime('%m'))
            da = int(datetime.date.today().strftime('%d'))
            d =datetime.date(yr,mo,da)
            current_date = d.strftime('%y%m%d')
            order_number = current_date+str(data.id)
            data.order_number =order_number
            data.save()

            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'tax':tax,
                'grand_total':grand_total,
                'total':total
            }
            return render(request,'orders/payments.html',context)
    else:
        return redirect('checkout') 


def order_complete(request):
    order_number = request.GET.get('order_number')
    print(order_number)
    trans_id = request.GET.get('payment_id')
    print(trans_id)
    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        print(order)
        order_product = OrderProduct.objects.filter(order_id=order.id)
        print(order_product)
        subtotal = 0
        for i in order_product:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id =trans_id)

        context = {
            'order':order,
            'trans_id':payment.payment_id,
            'order_product':order_product,
            'subtotal':subtotal,
            'payment' :payment,
            'order_number':order.order_number,

        }
        return render(request,'orders/order_complete.html',context)
    except(Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')