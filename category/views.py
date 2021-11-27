from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from store.models import Product
from category.models import Category
from cart.models import *
from django.db.models import Q

def category(request, category_slug=None):
    categories = None
    products = None
    category = Category.objects.all()
    if category_slug != None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories, is_available=True)
        product_count=products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = Product.objects.count()

    
    context = {'products': products, 'product_count': product_count, 'categories':category,'title': 'title'}
    return render(request, 'category_detail.html', context)
