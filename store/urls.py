from django.urls import path
from .views import all_products, filter_price_range, store,product_detail, search, filter_category
app_name='store'

urlpatterns = [
    path('',store, name='store'),
    path('category/<slug:category_slug>/',store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>',product_detail, name='product_detail'),
    path('search/', search, name='search'),
    path('all-products/',all_products, name='all_products'),
    path('filter/',filter_category, name='filter'),
    path('filter-price/',filter_price_range, name='filter_price_range'),
    
]