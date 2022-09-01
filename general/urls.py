from django.urls import path
from .views import *
app_name = 'general'

urlpatterns = [
    path('about-us',aboutUs, name='about_us' ),
    path('contact-us/', contact_page, name='contact_us'),
    
]