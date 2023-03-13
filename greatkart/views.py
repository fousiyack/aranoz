from django.shortcuts import render
from store.models import Product
from category.models import Category


def home(request):  
    products=Product.objects.all().filter(is_available="True")
    product_count=products.count()
    context={'products':products,
             'product_count':product_count,
             }
    print(context)
    return render(request,'home.html',context)

def categories(request):
    category=Category.objects.all()
    category_count=category.count()
    context={'category':category}
    return render(request,'home.html',context)

