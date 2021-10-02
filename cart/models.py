from accounts.models import Account
from django.db import models
from store.models import Product
# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user=models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.product.name

    def sub_total(self):
        return self.quantity*self.product.price
