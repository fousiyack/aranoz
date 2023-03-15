"""greatkart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views
# import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('store/',include('store.urls')),
    path('accounts/',include('accounts.urls')),
    path('category/', include('category.urls')),
    path('cart/',include('carts.urls')), 
    # path('categories/',views.categories,name='categories'),
    path('adminp/', include('adminp.urls')),
    path('orders/', include('orders.urls')),
    path('address/', include('address.urls')),
    path('adminpanel/', include('adminpanel.urls')),
    # path('__debug__/', include('debug_toolbar.urls')),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)