from django.urls import path
from .views import *

app_name = 'authentication'
urlpatterns=[
     path('customer_register/',customer_register.as_view(), name='customer_register'),
     path('login/',login_request, name='login'),
     path('logout/',logout_view, name='logout'),
]