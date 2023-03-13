from time import timezone
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from  store.models import Product
from .models import CartItem,Wishlist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import  JsonResponse
import json

from datetime import datetime
from orders.models import Address
from accounts.models import UserProfile
from adminp.models import Coupon

@login_required(login_url='login')
def add_to_cart(request, product_id):
    # Get the product and the user
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    
    # Check if the user is authenticated
    if user.is_authenticated:
        # Check if the user already has this product in their cart
        cart_item = CartItem.objects.filter(user=user, product=product).first()
        
        if cart_item is not None:
            # If the product is already in the cart, increment the quantity
            cart_item.quantity += 1
            cart_item.save()
        else:
            # If the product is not in the cart, create a new cart item
            CartItem.objects.create(user=user, product=product)
        
        # Redirect the user to the cart page
        return redirect('cart')
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect('login')


  
   
def remove_cart_products(request,product_id):
    user = request.user
    product=get_object_or_404(Product,id=product_id)  
    cart_item=CartItem.objects.get(product=product,user=user) 
    cart_item.delete()
    return redirect('cart') 

@login_required
def remove_cart_item(request,product_id,cart_item_id):
    user = request.user
    cart_items = CartItem.objects.filter(user=user,product=product_id,id=cart_item_id)
   
    for cart_item in cart_items:
        if cart_item.quantity == 1:
            cart_item.delete()  # remove the item from the cart if the quantity is 1
        else:
            cart_item.quantity -= 1
            cart_item.save()  # decrement the quantity by 1
    return redirect('cart')
         
def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        sub_total=0
        user=request.user
        cart_items=CartItem.objects.filter(user=user)
        for cart_item in cart_items:
            sub_total=(cart_item.product.price*cart_item.quantity)
            total+=sub_total
            quantity+=cart_item.quantity
            cart_item.sub_total = sub_total
        tax=(2 * total)/100
        grand_total=total+tax   
        
        request.session['grand_total']=grand_total
                
          
        
    except ObjectDoesNotExist:
        pass
    context={
        'sub_total':sub_total,
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
        
    }        
   
    return render(request,'store/cart.html',context)


    
    
         
# def wishList(request):
#         user=request.user
#         wish_items=WishItem.objects.filter(user=user)
#         context={
#         'wish_items':wish_items 
#          }        
   
#         return render(request,'store/wishlist.html',context)



    
#@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        user=request.user
        grand_total=0
        tax=0
        
        rowcart=CartItem.objects.filter(user=user)
        for item in rowcart:
            if item.quantity>item.product.stock:
                cartitem=CartItem.objects.filter(id=item.id)
                cartitem.delete()
        
        cart_items=CartItem.objects.filter(user=user)
        for cart_item in cart_items:
            sub_total=(cart_item.product.price*cart_item.quantity)
            total+=sub_total
            quantity+=cart_item.quantity
            cart_item.sub_total = sub_total
            
        tax=(2 * total)/100
        grand_total=total+tax      
        #userprofile=Profile.objects.filter(user=request.user).first()
        address=Address.objects.filter(user=request.user).first()
        if request.POST.get('coupon') is None: 
             request.session['coupon_id']=""
    except ObjectDoesNotExist:
        pass
    context={
        'sub_total':sub_total,
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'userprofile':address
        
    } 
    return render(request,'store/checkout.html',context)


def wishlist(request):
    user = request.user
    
    witems=Wishlist.objects.filter(user=user)
    witem_count = witems.count()
    
    context={
        'witems':witems,
        'witem_count':witem_count,
    }
    return render(request,'store/wishlist.html',context)

def add_to_wish(request,product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=product_id)
        user = request.user
        
        if Wishlist.objects.filter(product=product,user=user).exists():
            return redirect('wishlist')
        
        else:
            Wishlist.objects.create(product=product,user=user)
            return redirect('wishlist')
    else:
        return redirect('login')
    
def remove_wish_item(request,product_id):
    wishItem=Wishlist.objects.get(pk=product_id)
    wishItem.delete()
    return redirect('wishlist') 



def validate_coupon(request):
  if request.method =='POST': 
    coupon_code = request.GET.get('coupon')
    user = request.user
    try:
        coupon = Coupon.objects.get(coupon_code=coupon_code)
        #console.log(coupon)
        minimum = coupon.minimum_purchase_amount
        items=CartItem.objects.filter(user=user)
        total =0
        g_total=0
        tax=0
        
        body = json.loads(request.body)
        coupon_id = body['coupon']
        for i in range(len(items)):
                x = items[i].product.price*items[i].quantity
                total = total+x
                
        # if coupon.expiry_date <  datetime.now().date():
        #     messages.error(request,'Coupon has expired') 
        #     return redirect('cart')
        # elif total < coupon.minimum_purchase_amount:
        #     messages.error(request,'Minimum purchase amount for this coupon is',minimum) 
        #     return redirect('cart')
        # else:
        discount = int(total) * coupon.discount_percentage / 100
        tax = round((2 * total)/100)
        g_total = total + tax        
        return JsonResponse({
             'discount' : discount,
             'amount':total,
             'coupon_id': coupon_id,
             'g_total': g_total,
             'coupon_name': coupon_id

        })
       
            
        messages.success(request,'Coupon applied successfully')
    except Coupon.DoesNotExist:
        messages.error(request,'Invalid coupon code')

    return redirect('orders')



@login_required(login_url = 'login')
def apply_coupon(request):


    if request.method == 'POST':
        # Get the coupon code from the form
        coupon_code = request.POST.get('coupon')
        request.session['coupon_id']=coupon_code 
        
        cart_items   = CartItem.objects.filter(user=request.user)
        total = 0
        grand_total=0
        tax=0
        discount=0
        for cart_item in cart_items:
            total    += (cart_item.product.price * cart_item.quantity)
        tax = (2 * total) / 100
        grand_total = tax + total    
        # Validate the coupon code
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            request.session['coupon_applied'] = True
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            return JsonResponse({'grand_total': grand_total,'discount':discount,'coupon_code':coupon_code})

        # Apply the discount to the  total  
        discount =grand_total* coupon.discount_percentage/100
        grand_total=grand_total-discount
        coupon_code=coupon_code
        
        # messages.success(request, 'Coupon applied successfully.')

        return JsonResponse({'grand_total': grand_total,'discount':discount,'coupon_code':coupon_code})

    return JsonResponse({'error': 'Invalid request method'})
    
  
              
