from django.urls import path
from . import views
app_name = 'coupons'
urlpatterns = [
   
    path('wallet_balance',views.wallet_balance, name="wallet_balance"),
    
    path('coupon_list', views.coupon_list, name='coupon_list'),
    path('coupon_create/', views.coupon_create, name='coupon_create'),
    path('<int:pk>/', views.coupon_detail, name='detail'),
    path('<int:pk>/update/', views.coupon_update, name='update'),
    path('<int:pk>/delete/', views.coupon_delete, name='delete'),
]
