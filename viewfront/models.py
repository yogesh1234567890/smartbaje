from django.db import models

# Create your models here.

class Category(models.Model):

    class Meta:
        verbose_name_plural="Categories"

    def __str__(self):
        return self.name

    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500,null=True,blank=True)
    image = models.ImageField(upload_to="categories",null=True,blank=True)
    slug=models.SlugField(max_length=100, unique=True)




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
    ratings = models.FloatField(null=True,blank=True)

