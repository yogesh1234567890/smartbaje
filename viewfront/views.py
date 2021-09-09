from django.shortcuts import render
from .models import *
# Create your views here.

def viewpage(request):
    products=Product.objects.all()
    categories=Category.objects.all()
    context={
        'categories':categories,
        'products':products
    }
    return render(request,"viewfront/index-4.html",context)

