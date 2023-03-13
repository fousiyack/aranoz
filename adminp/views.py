from django.shortcuts import render, redirect,get_object_or_404
from .forms import CouponForm
from .models import Coupon,Wallet


def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CouponForm()
    return render(request, 'add_coupon.html', {'form': form})



def wallet_balance(request):
    wallet = Wallet.objects.get(user=request.user)
    
    return render(request,'accounts/wallet.html', {'wallet': wallet})    

def coupon_list(request):
    coupons = Coupon.objects.all()
    
    return render(request, 'manager/coupon_list.html', {'coupons': coupons})

def coupon_detail(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    return render(request, 'coupon_detail.html', {'coupon': coupon})

def coupon_create(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupons:coupon_list')
    else:
        form = CouponForm()
    return render(request, 'manager/coupon_form.html', {'form': form})

def coupon_update(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('coupons:coupon_list')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'manager/coupon_form.html', {'form': form})

def coupon_delete(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        coupon.delete()
        return redirect('coupons:coupon_list')
    return render(request, 'manager/coupon_confirm_delete.html', {'coupon': coupon})
