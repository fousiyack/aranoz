from django.db import models
from accounts.models import Account
from store.models import Product


class Order(models.Model):
   
    user=models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    #payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    Order_number=models.CharField(max_length=20)
    
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    email=models.EmailField(max_length=50)
    address_line_1=models.CharField(max_length=255)
    address_line_2=models.CharField(max_length=255)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    zip_code=models.CharField(max_length=10, null=True)
    
    order_note=models.CharField(max_length=255)
    
    total_price=models.FloatField()
    coupon=models.CharField(max_length=100,null=True)
    payment_mode=models.CharField(max_length=150,null=False)
    payment_id=models.CharField(max_length=100,null=True)
    tracking_no=models.CharField(max_length=150,null=True)
    orderstatuses={
        ('Order Placed','Order Placed'),
        ('Out For Shipping','Out For Shipping'),
        ('completed','completed'),
       
    }
    status=models.CharField(max_length=150,choices=orderstatuses,default='Order Placed')
    message=models.TextField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
    
    def full_name(self):
        return f'{self.first_name}{self.last_name}'
    
    def __str__(self):
        return '{} - {}'.format(self.id,self.tracking_no)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    price= models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return'{} {}'.format(self.order.id, self.order.tracking_no)    


class Address(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone = models.CharField(max_length=15,null=False)
    email=models.CharField(max_length=150,null=True)
    address_line_1= models.TextField(max_length=150,null=False)
    address_line_2= models.TextField(max_length=150,null=True)
    city = models.CharField(max_length=150,null=False)
    state = models.CharField(max_length=150,null=False)
    country = models.CharField(max_length=150,null=False)
    zip_code=models.CharField(max_length=10,null=False)
    created_at =models.DateTimeField(auto_now_add=True)
    is_default=models.BooleanField(default=False)
    
    

    def __str__(self):
        return self.user.username    
    