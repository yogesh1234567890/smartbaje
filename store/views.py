from django.http.response import HttpResponse
from cart.views import _cart_id
from django.shortcuts import get_object_or_404, render
from store.models import Product
from category.models import Category
from cart.models import *
from django.db.models import Q

def store(request, category_slug=None):
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

    
    context = {
        'products': products, 
        'product_count': product_count, 
        'title': 'title'
        }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product=single_product).exists()
        # accessing fk value with __
       
    except Exception as e:
        raise e

    context={'single_product':single_product,'in_cart':in_cart}
    return render(request,'store/product-detail.html',context)

def search(request):
    if 'search_keyword' in request.GET:
        search_keyword = request.GET['search_keyword']
        if search_keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=search_keyword)|Q(name__icontains=search_keyword))
            product_count = products.count()
    context = {
        'title': 'Search',
        'products': products,
        'search_products_count': product_count,
        }
    return render(request, 'store/store.html', context)