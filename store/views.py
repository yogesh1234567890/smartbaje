from django.http.response import HttpResponse
from django.db.models import Max
from cart.views import _cart_id
from django.shortcuts import get_object_or_404, render
from general.models import Brand
from store.models import Product, ProductOffers,DealsAndPromotions
from category.models import Category
from cart.models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def store(request, category_slug=None):
    try:
        categories = None
        products = None
        category = Category.objects.all()
        Product_offers = ProductOffers.objects.all()
        promotions = DealsAndPromotions.objects.all()
        brands = Brand.objects.all()
        if category_slug != None:

            categories=get_object_or_404(Category,slug=category_slug)
            products=Product.objects.filter(category=categories, is_available=True)
            product_count=products.count()
        else:

            products = Product.objects.all().filter(is_available=True)
            print("error------------------------------------")
            # product_count = Product.objects.count()
            product_count = products.count()

        
        context = {
            'products': products, 
            'product_count': product_count, 
            'title': 'title',
            'categories': category,
            'Product_offers': Product_offers,
            'promotions': promotions,
            'brands': brands,
            }

    except Exception as e:
        context = {}
        print("Error Occured::: {}".format(e))
        
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug, slug=product_slug)
        products=Product.objects.filter(category__slug=category_slug, is_available=True)
        in_cart = CartItem.objects.filter(cart__cart = _cart_id(request), product=single_product).exists()
        # accessing fk value with __
       
    except Exception as e:
        raise e

    context={
        'single_product':single_product,
        'in_cart':in_cart,
        'products': products,
    }
    return render(request,'store/product-detail.html',context)

def search(request):
    if 'search_keyword' in request.GET:
        search_keyword = request.GET['search_keyword']
        if search_keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=search_keyword)|Q(name__icontains=search_keyword))
            product_count = products.count()
    category = Category.objects.all()
    Product_offers = ProductOffers.objects.all()
    promotions = DealsAndPromotions.objects.all()
    context = {
        'title': 'Search',
        'products': products,
        'search_products_count': product_count,
        'Product_offers': Product_offers,
        'promotions': promotions,
        }
    return render(request, 'store/store.html', context)

def all_products(request):
    try:
        products = Product.objects.all()
        product_count = Product.objects.count()
        brands = Brand.objects.all()
        promotions = DealsAndPromotions.objects.all()
        Product_offers = ProductOffers.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 6)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        slider_price = Product.objects.aggregate(Max('price'))
    except Exception as e:
        print("Error Occured::: {}".format(e))
    context = {
        'title': 'All Products',
        'products': products,
        'brands': brands,
        'product_count': product_count,
        'Product_offers': Product_offers,
        'promotions': promotions,
        'slider_max_price': slider_price.get("price__max"),
        }
    return render(request, 'store/all_products.html', context)

def filter_category(request):
    if request.is_ajax():
        data=request.body.decode('utf-8')
        cat_id = data[-1]
        products = Product.objects.filter(category_id=cat_id)
        product_count = products.count()
        return render(request, 'store/filter.html', {'products': products, 'product_count': product_count})
    
    
def filter_brand(request):
    if request.is_ajax():
        data=request.body.decode('utf-8')
        brand_id = data[-1]
        products = Product.objects.filter(brand_id=brand_id)
        product_count = products.count()
        return render(request, 'store/filter.html', {'products': products, 'product_count': product_count})
    
    
    
def filter_price_range(request):
    if request.is_ajax():
        data=dict(request.POST.lists())
        range=data['value[]']
        asa=[]
        for i in range:
            a=[int(s) for s in i.split() if s.isdigit()]
            asa.append(a[0])
        products = Product.objects.filter(price__gte=asa[0], price__lte=asa[1])
        print(products)
        product_count = products.count()
        return render(request, 'store/filter.html', {'products': products, 'product_count': product_count}) 