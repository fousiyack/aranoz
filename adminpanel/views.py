from django.shortcuts import render,redirect
from accounts.views import logout
from store.models import Product
from django.core.paginator import Paginator
from django.db.models import Q 
from adminpanel.forms import ProductForm, CategoryForm
from category.models import Category
from accounts.models import Account
from orders.models import Order,OrderItem

from django.views.generic import View
from django.http import JsonResponse


from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from django.db.models.functions import TruncDay


# Create your views here.
def adminHome(request):
    return render(request, 'admin/admin_base.html')

def admin_dashboard(request):
    if request.user.is_admin:
        user_count = Account.objects.filter(is_admin=False).count()
        category_count = Category.objects.all().count()
        product_count=Product.objects.all().count()
        order_count=Order.objects.all().count()


        context = {
            'user_count'    : user_count,
            'category_count':category_count,
            'product_count':product_count,
            'order_count':order_count
            

        }
    return render(request,'admin/admin_dashboard.html',context)

def manage_product(request):
    if request.user.is_admin:
        if request.method == 'POST':
            keyword = request.POST['keyword'] 
            products = Product.objects.filter(Q(product_name__icontains=keyword) | Q(slug__icontains=keyword) | Q(category__category_name__icontains=keyword)).order_by('id')

        else:
            products = Product.objects.all().order_by('id')

        paginator = Paginator(products, 10)
        page      = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = {
            'products' : paged_products 
        }
        return render(request, 'manager/product_management.html', context)

    else:
        return redirect('home')
def add_product(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save() 
                return redirect('manage_product')
            else:
              print(form.errors)
              form = ProductForm()
              context = {
                  'form' : form
              }
              return render(request, 'manager/add_product.html', context)
        else:
            form = ProductForm()
            context = {
                'form' : form
            }
            return render(request, 'manager/add_product.html', context)

    else:
        return redirect('home')
    
def edit_product(request, product_id):
    if request.user.is_admin:
        product = Product.objects.get(id=product_id)
        form = ProductForm(instance=product)

        if request.method == 'POST':
            try:
                form =ProductForm(request.POST, request.FILES, instance=product)
                if form.is_valid():
                    form.save()

                    return redirect('manage_product')

            except Exception as e:
                raise e

        context = {
            'product' : product,
            'form' : form
        }
        return render(request, 'manager/edit_product.html', context)

    else:
        return redirect('home')   
    
def delete_product(request, product_id):
    if request.user.is_admin:
        product = Product.objects.get(id=product_id)
        product.delete()
        return redirect('manage_product')

    else:
        return redirect('home')    
    
def manage_category(request):
    if request.user.is_admin:
        if request.method == 'POST':
            keyword = request.POST['keyword']
            categories = Category.objects.filter(Q(category_name__icontains=keyword) | Q(slug__icontains=keyword)).order_by('id') 
        
        else:
            categories = Category.objects.all().order_by('id')

        paginator = Paginator(categories, 10)
        page = request.GET.get('page')
        paged_categories = paginator.get_page(page)

        context = {
            'categories': paged_categories
        }

        return render(request, 'manager/category_management.html', context)

    else:
        return redirect('admin_dashboard')    
    
def add_category(request):
  if request.user.is_admin:
    form = CategoryForm()
    if request.method == 'POST':
     
        form = CategoryForm(request.POST, request.FILES)
        print(form)
        
        if form.is_valid():
            form.save()
            return redirect('manage_category')
        else:
              form = CategoryForm()   
              context = {
                  'form' : form
              }
              return render(request, 'manager/add_category.html', {'form': form})
    else:
              form = CategoryForm()   
              context = {
                  'form' : form
              }
              return render(request, 'manager/add_category.html', {'form': form})      
  
  else:
    return redirect('home')  


def edit_category(request, category_id):
    if request.user.is_admin:
        category = Category.objects.get(id=category_id)
        form = CategoryForm(instance=category)

        if request.method == 'POST':
            try:
                form =CategoryForm(request.POST, request.FILES, instance=category)
                if form.is_valid():
                    form.save()

                return redirect('manage_category')

            except Exception as e:
                raise e

        context = {
            'category' : category,
            'form' : form
        }
        return render(request, 'manager/edit_category.html', context)

    else:
        return redirect('home') 
    
# @never_cache
# @login_required(login_url='manager_login')
def delete_category(request, category_id):
   if request.user.is_admin:
        category = Category.objects.get(id=category_id)
        category.delete()

        return redirect('manage_category')

   else:
       return redirect('admin_dashboard')
   

# @never_cache
# @login_required(login_url='manager_login')
def manage_user(request):
  if request.user.is_admin:
    if request.method == 'POST':
      keyword = request.POST['keyword']
      users = Account.objects.filter(Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(username__icontains=keyword) | Q(email__icontains=keyword) | Q(phone_number__icontains=keyword)).order_by('id')
    
    else:
        users = Account.objects.filter(is_admin=False).order_by('id')

    paginator   = Paginator(users, 10) 
    page        = request.GET.get('page')
    paged_users = paginator.get_page(page)

    context = {
        'users' : paged_users,
    }
    return render(request, 'manager/user_management.html', context)

  else:
    return redirect('admin_dashboard') 

#BAN User
# @never_cache
# @login_required(login_url='manager_login')
def ban_user(request, user_id):
    if request.user.is_admin:
        user = Account.objects.get(id=user_id)
        user.is_active = False
        user.save()

        return redirect('manage_user')

    else:
        return redirect('home')


#UnBAN User
# @never_cache
# @login_required(login_url='manager_login')
def unban_user(request, user_id):
    if request.user.is_admin:
        user = Account.objects.get(id=user_id)
        user.is_active = True
        user.save()

        return redirect('manage_user')

    else:
        return redirect('home')
       
def order_management(request):
  if request.user.is_superadmin:
    if request.method == 'POST':
        key = request.POST['keyword']
        order = Order.objects.filter( Q(tracking_no__startswith=key) | Q(total_price__startswith=key) | Q(first_name__startswith=key)).order_by('-id')
    else:
        order = Order.objects.all().order_by('-id') 
    paginator = Paginator(order, 10)
    page = request.GET.get('page')
    paged_order = paginator.get_page(page)

    context = {
        'order': paged_order
        }
    return render(request, 'manager/order_management.html',context)
  else:
    return redirect('index') 


 
def manager_vieworder(request,tracking_no):
  if request.user.is_superadmin:
    order = Order.objects.filter(tracking_no=tracking_no).first()
    orderitems = OrderItem.objects.filter(order=order)
    context={
        'order': order,
        'orderitems':orderitems,
    }
    return render(request,'manager/manager_vieworder.html',context)
  else:
    return redirect('home') 



#ACCEPT ORDER
def manager_accept_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Out For Shipping'
    order.save()
    return redirect('order_management')  

#SHIP ORDER    
def manager_ship_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Shipped'
    order.save()
    return redirect('order_management')

#DELIVERED ORDER
def manager_delivered_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Delivered'
    order.save()
    return redirect('order_management')          

#CANCEL ORDER
def manager_cancel_order(request,tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Cancelled'
    order.save()
    return redirect('order_management')

# @never_cache
def manager_logout(request):
    logout(request)
    return redirect('login')

def ChartData(request):
    # def get(self, request, *args, **kwargs):
        user_count = Account.objects.filter(is_admin=False).count()
        category_count = Category.objects.all().count()
        product_count=Product.objects.all().count()
        order_count=Order.objects.all().count()
        data = {
            'labels': ['Orders', 'Products', 'Users', 'Categories'],
            'data': [order_count, product_count, user_count, category_count],
        }
        return JsonResponse(data)
    


def daily_orders_chart(request):
    today = timezone.now().date()
    last_week = today - timedelta(days=7)
    orders = Order.objects.filter(created_at__gte=last_week, created_at__lte=today)\
                          .annotate(day=TruncDay('created_at'))\
                          .values('day')\
                          .annotate(order_count=Count('id'))\
                          .order_by('day')

    orders_data = list(orders)

    return render(request, 'admin/admin_dashboard.html', {'orders_data': orders_data})