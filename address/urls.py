from django.urls import path
from . import views

app_name = 'address'
urlpatterns = [
    path('address_list/', views.AddressListView.as_view(), name='address_list'),
    path('addresslist/', views.addresslist, name='addresslist'),
    path('create/', views.AddressCreateView.as_view(), name='address_create'),
    path('<int:pk>/', views.AddressUpdateView.as_view(), name='address_update'),
    path('<int:pk>/delete/', views.AddressDeleteView.as_view(), name='address_delete'),
]