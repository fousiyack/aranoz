from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',views.remove_cart_item,name='remove_cart_item'),
    path('remove_cart_products/<int:product_id>/',views.remove_cart_products,name='remove_cart_products'),
    path('checkout',views.checkout,name="checkout"),
    
    
    path('add_to_wish/<int:product_id>/',views.add_to_wish,name='add_to_wish'),
    path('remove_wish_item/<int:product_id>/',views.remove_wish_item,name='remove_wish_item'),
    path('validate_coupon/',views.validate_coupon,name='validate_coupon'),
    path('apply_coupon/',views.apply_coupon,name='apply_coupon'),
    

   
   
   
]

