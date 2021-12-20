from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Welcome to Smart Baje Administrator"
admin.site.site_title = "Welcome to Samrt Baje Administrator"
admin.site.index_title = "Welcome to Administrator Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls'),name='store'),
    path('cart/', include('cart.urls'),name='cart'),
    path('auth/', include('accounts.urls'), name="auth"),
    path('accounts/', include('allauth.urls')),
    # path('oauth/', include('social_django.urls', namespace='social')),
    path('orders/', include('orders.urls'), name="orders"),
    path('category/', include('category.urls'), name="category"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
