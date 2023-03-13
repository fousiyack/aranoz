from django.db import models
from accounts.models import Account
from django import forms


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.FloatField()
    expiry_date = models.DateField()
    minimum_purchase_amount = models.FloatField()
    def __str__(self):
        return self.coupon_code
    widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
class CouponUser(models.Model):
    coupon_code = models.CharField(max_length=30)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
        
    
class Wallet(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)    
    
    