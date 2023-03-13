from django.shortcuts import render
from . models import Category

def categories(request):
    category=Category.objects.all()
    category_count=category.count()
    context={'category':category}
    return render(request,'store/category.html',context)


