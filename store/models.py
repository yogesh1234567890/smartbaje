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
    description = models.TextField(max_length=500,null=True,blank=True)
    image = models.ImageField(upload_to="products")
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    ratings = models.FloatField(null=True,blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateField(auto_now=True)

    def get_url(self):
        return reverse('store:product_detail',args=[self.category.slug,self.slug])