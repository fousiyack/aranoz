from django.db import models
from store.models import Product
from accounts.models import Account
 





class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
   
    
class Wishlist(models.Model):
    user=models.CharField(max_length=100,null=False)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    
    

