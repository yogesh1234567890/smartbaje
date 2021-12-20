from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.
class Product(models.Model):

    class Meta:
        verbose_name_plural="Products"

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField()
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="products")
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    ratings = models.FloatField(null=True,blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateField(auto_now=True)

    def get_url(self):
        return reverse('store:product_detail',args=[self.category.slug,self.slug])

class ProductOffers(models.Model):
    offer_choices=(
        ('Smart Offer','Smart Offer'),
        ('Time Deals','Time Deals'),
        ('Clearance','Clearance'),
    )
    class Meta:
        verbose_name_plural = 'Product Offers'
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    offer_name = models.CharField(choices=offer_choices,max_length=100)
    offer_description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.offer_name + " " + self.product.name

class DealsAndPromotions(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to="deals")
    discounted_price = models.FloatField(null=True,blank=True)
    offer_description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.offer_description

