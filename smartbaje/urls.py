from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.admin.sites import AdminSite

from general.views import handle_404
admin.site.site_header = "Smart Deals Nepal"
admin.site.site_title = "Smart Deals Nepal"
admin.site.index_title = "Smart Deals Nepal "

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls'),name='store'),
    path('cart/', include('cart.urls'),name='cart'),
    path('auth/', include('accounts.urls'), name="auth"),
    path('accounts/', include('allauth.urls')),
    # path('oauth/', include('social_django.urls', namespace='social')),
    path('orders/', include('orders.urls'), name="orders"),
    path('category/', include('category.urls'), name="category"),
    path('general/', include('general.urls'), name="general"),
    path('summernote/', include('django_summernote.urls')),
    
]
AdminSite.index_template = 'admin/index.html'
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

handler404 = handle_404