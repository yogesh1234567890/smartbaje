from django.db import models

# Create your models here.
class CustomerQuery(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    subject = models.TextField()
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=100)
    file = models.ImageField(upload_to='brand/')
    
    def __str__(self) -> str:
        return self.name