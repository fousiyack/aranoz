from django import forms
from .models import Coupon

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'discount_percentage', 'expiry_date', 'minimum_purchase_amount']
        
