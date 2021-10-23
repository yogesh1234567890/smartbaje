from django.urls import path
from .views import category

app_name='category'

urlpatterns = [
    # path('',cat, name='store'),
    path('<slug:category_slug>/',category, name='products_by_category'),
   
]