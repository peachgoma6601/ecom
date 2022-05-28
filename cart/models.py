from django.db import models
from store.models import Product,ProductVariation
from accounts.models import Account
# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=50,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cart_id)

class CartItems(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_variation = models.ManyToManyField(ProductVariation,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price*self.quantity

    def __str__(self):
        return str(self.product)

