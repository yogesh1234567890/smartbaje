from accounts.models import Account
from django.db import models
from store.models import Product, Variation
# Create your models here.
class Cart(models.Model):
    cart=models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart


class CartItem(models.Model):
    user=models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.product.name

    def sub_total(self):
        return self.quantity*self.product.price
