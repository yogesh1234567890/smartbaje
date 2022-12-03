from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):

    class Meta:
        verbose_name_plural="Product Categories"

    def __str__(self):
        return self.name

    name=models.CharField(max_length=100)
    description=models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="categories",null=True,blank=True)
    slug=models.SlugField(max_length=100, unique=True)

    def get_url(self):
        return reverse('store:products_by_category',args=[self.slug])