from django.forms import DecimalField
from django.shortcuts import render,redirect
from carts.models import CartItem
from greatkart import settings
from .forms import OrderForm
from .models import Order,Address,OrderItem
from store.models import Product
import datetime
from django.http import HttpResponse ,JsonResponse
import json
from accounts.models import UserProfile

from django.contrib.auth.decorators import login_required
from . models import Address
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
import random
from accounts.models import Account
from django.contrib import messages
from adminp.models import Coupon,Wallet
from decimal import Decimal
from django.core.paginator import Paginator
# Create your views here.
import razorpay
from django.core.mail import send_mail

@never_cache
@login_required(login_url=('login')) 
def place_order(request):
    if request.method =='POST':
        cart_items   = CartItem.objects.filter(user=request.user.id)
        if not cart_items:
            return redirect('store')

        # currentuser = Account.objects.filter(id=request.user.id).first()
        # if not currentuser.first_name :
        #     currentuser.first_name = request.POST.get('first_name')# type: ignore
        #     currentuser.last_name = request.POST.get('last_name')# type: ignore
        #     currentuser.save()# type: ignore
        
        if not Address.objects.filter(user=request.user):
            userprofile = Address()
            userprofile.user = request.user
            userprofile.first_name = request.POST.get('first_name')
            userprofile.last_name = request.POST.get('last_name')
            userprofile.phone = request.POST.get('phone')
            userprofile.email=request.POST.get('email')
            userprofile.address_line_1 = request.POST.get('address_line_1')
            userprofile.address_line_2 = request.POST.get('address_line_2')
            userprofile.city = request.POST.get('city')
            userprofile.state= request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.zip_code = request.POST.get('zip_code')
            userprofile.save()   
             

        newOrder =Order()
        newOrder.user=request.user
        newOrder.first_name = request.POST.get('first_name')
        newOrder.last_name = request.POST.get('last_name')
        newOrder.email = request.POST.get('email')
        newOrder.phone = request.POST.get('phone')
        newOrder.address_line_1 = request.POST.get('address_line_1')
        newOrder.address_line_2 = request.POST.get('address_line_2')
        newOrder.city = request.POST.get('city')
        newOrder.state= request.POST.get('state')
        newOrder.country = request.POST.get('country')
        newOrder.zip_code = request.POST.get('zip_code')
        newOrder.payment_mode = request.POST.get('payment_mode')
        if('payment_id' in request.POST ):
            newOrder.payment_id = request.POST.get('payment_id')
        else:
          yr = int(datetime.date.today().strftime('%Y'))
          dt = int(datetime.date.today().strftime('%d'))
          mt = int(datetime.date.today().strftime('%m'))
          d = datetime.date(yr,mt,dt)
          current_date = d.strftime("%Y%m%d")
          order_number = 'brotoz'+ current_date
          newOrder.payment_id = order_number
        
      
        
        
          #taking total price
        cart_items   = CartItem.objects.filter(user=request.user)
        total = 0
        grand_total=0
        tax=0
        for cart_item in cart_items:
            total    += (cart_item.product.price * cart_item.quantity)

        tax = (2 * total) / 100
        grand_total = tax + total
        
        print(request.session['coupon_id'])
        
        if request.session['coupon_id']:
            coupons = Coupon.objects.get(coupon_code=request.session['coupon_id'])
            discount = int(grand_total) * coupons.discount_percentage / 100
            grand_total=int(grand_total)-int(discount)
            newOrder.coupon = request.session['coupon_id']
        else:
            newOrder.coupon ="None"     
        newOrder.total_price = grand_total 
        trackNo = 'brotoz'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackNo) is None:
            trackNo = 'brotoz'+str(random.randint(1111111,9999999))
        newOrder.tracking_no=trackNo
        newOrder.sub_total=total
        newOrder.tax=tax
        newOrder.save()
        
        

        newOrderItems = CartItem.objects.filter(user=request.user)
        for item in newOrderItems:
            OrderItem.objects.create(
                order = newOrder,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
                user=request.user
            )
            #TO DECRESE THE QUANTITY OF PRODUCT
            orderproduct = Product.objects.filter(id=item.product_id).first() # type: ignore
            orderproduct.stock -=  item.quantity # type: ignore
            orderproduct.save() # type: ignore
        
            
        # TO CLEAR THE USER'S CART
        cart_item=CartItem.objects.filter(user=request.user)
        cart_item.delete()
        if 'coupon_id' in request.session:
            del request.session['coupon_id']
        messages.success(request,'Order Placed Successfully')
        
        payMode =  request.POST.get('payment_mode')
    
        if (payMode == "Paid by Razorpay" ):
           return JsonResponse ({'status':"Your order has been placed successfully"})
        elif (payMode == "COD" ):
            return redirect('cod_order_complete')
        #return redirect('myorder')
        
    return redirect('checkout') 


@never_cache
@login_required(login_url=('login'))  # type: ignore
def razorpaycheck(request):
    cart = CartItem.objects.filter(user=request.user)  
    total_price = 0 
    if cart:
            
        for item in cart:
            total_price   += total_price + item.product.price * item.quantity 
        tax = round((2 * total_price)/100)
        grand_total = total_price + tax
        if request.session['coupon_id']:    
            coupons = Coupon.objects.get(coupon_code=request.session['coupon_id'])
            discount = int(grand_total) * coupons.discount_percentage / 100
            grand_total=int(grand_total)-int(discount)
        return JsonResponse({
            'total_price' : grand_total
        })
    else:
        return redirect('store')
    
    




@never_cache
@login_required(login_url=('login')) 
def myorder(request):
    orders=Order.objects.filter(user=request.user).order_by('-created_at')
    paginator=Paginator(orders,10)
    page=request.GET.get('page')
    paged_orders=paginator.get_page(page)
    context ={
        'orders':paged_orders
    }    
    return render(request,'orders/myorder.html',context)

@never_cache
@login_required(login_url=('login')) 
def vieworder(request,tracking_no):
    order =Order.objects.filter(tracking_no=tracking_no,user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context={
        'order': order,
        'orderitems':orderitems,
        
    }
    return render(request,'orders/vieworder.html',context)




def order_complete(request):
     
    payment_id = request.GET.get('payment_id')
    print(payment_id)
    order_details = Order.objects.get(payment_id=payment_id)
    orderitems = OrderItem.objects.filter(order=order_details.id)
     
    context={
        'orders': order_details,
        'orderitems':orderitems,
         
    }
        
    return render(request, 'orders/order_complete.html',context)
def cod_order_complete(request): 
   #order =Order.objects.filter(tracking_no=tracking_no,user=request.user).first()
   
   return render(request,'orders/cod_order_complete.html')

#def Coupon_User(request): 
    
   



def cancel_order(request,tracking_no) :
    current_user=request.user
    order = Order.objects.get(tracking_no=tracking_no)
    if order.payment_mode=="COD":
       Order.objects.filter(user=current_user,tracking_no=tracking_no).update(status='Cancelled')
    else:   
        client = razorpay.Client(auth=("RAZOR_KEY_ID", "RAZOR_KEY_SECRET"))
        payment_id = order.payment_id
        amount = order.total_price
        amount=amount*100
        
        capturing_amount = client.payment.capture(payment_id,amount)
        if capturing_amount['status'] == 'captured':
            refund_data = {
            "payment_id":payment_id,
            "amount": amount,  
            "currency": "INR",    
                    }
            refund = client.payment.refund(payment_id, refund_data)
            if refund is not None:
                
                Order.objects.filter(user=current_user,tracking_no=tracking_no).update(status='Cancelled')
                mess=f'Hello\t{current_user.first_name},\nYour Product has been canceled,Money will be refunded with in 1 hour\nThanks!'
                send_mail(
                                "brotoz - Cancel Product",
                                mess,
                                settings.EMAIL_HOST_USER,
                                [current_user.email],
                                fail_silently = False
                                )
            else :
                pass
        else :
            pass
    return redirect('myorder')

