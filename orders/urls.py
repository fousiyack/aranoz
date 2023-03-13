from django.urls import path
from .import views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('proceed-to-pay',views.razorpaycheck,name="razorpaycheck"),
    path('myorder/', views.myorder, name='myorder'),
    path('cod_order_complete/', views.cod_order_complete, name='cod_order_complete'),
    path('vieworder/<str:tracking_no>/',views.vieworder, name='vieworder'),
    path('cancel_order/<str:tracking_no>/',views.cancel_order, name='cancel_order'),
    path('order-complete/',views.order_complete, name='order_complete '),
    #path('Coupon_User/',views.Coupon_User, name='Coupon_User ')
]