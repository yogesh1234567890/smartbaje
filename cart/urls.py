from django.urls import path
from .views import *
app_name = 'cart'

urlpatterns = [
    path('',cart, name='cart' ),
    path('add_cart/<int:product_id>/',add_cart, name='add_cart' ),
    
]