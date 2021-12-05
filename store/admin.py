from django.contrib import admin
from .models import Product, ProductOffers
from django.utils.html import format_html
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30">'.format(object.image.url))
    thumbnail.short_description = 'Product Image'
    list_display=('thumbnail','name','price','stock','category','modified_date','is_available')
    prepopulated_fields={'slug':('name',)}

admin.site.register(Product,ProductAdmin)

admin.site.register(ProductOffers)