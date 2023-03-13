from django.urls import path
from . import views 


urlpatterns = [
path('', views.adminHome, name="adminHome"),
path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),


path('manage_product/', views.manage_product, name='manage_product'),
path('add_product/', views.add_product, name='add_product'),  
path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),


path('manage_category/', views.manage_category, name='manage_category'),
path('add_category/', views.add_category, name='add_category'),
path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),


path('manage_user', views.manage_user, name="manage_user"),
path('ban_user/<int:user_id>/', views.ban_user, name='ban_user'),
path('unban-user/<int:user_id>/', views.unban_user, name='unban_user'),


path('order_management/', views.order_management, name="order_management"),
path('manager_vieworder/<str:tracking_no>/', views.manager_vieworder, name='manager_vieworder'),
path('manager_accept_order/<str:tracking_no>/', views.manager_accept_order, name='manager_accept_order'),
path('manager_ship_order/<str:tracking_no>/', views.manager_ship_order, name='manager_ship_order'),
path('manager_delivered_order/<str:tracking_no>/', views.manager_delivered_order, name='manager_delivered_order'),
path('manager_cancel_order/<str:tracking_no>/', views.manager_cancel_order, name='manager_cancel_order'),

path('manager_logout', views.manager_logout, name="manager_logout"),

path('chart_data/',views.ChartData, name='chart_data'),
]