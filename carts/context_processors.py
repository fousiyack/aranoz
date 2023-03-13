from . models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return{}
    else:
        try:
            if request.user.is_authenticated:
               cart_items = CartItem.objects.all().filter(user=request.user)

            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)



 
