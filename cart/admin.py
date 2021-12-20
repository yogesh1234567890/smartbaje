from django.contrib import admin
from .models  import *
from django.utils.html import format_html
# Register your models here.

admin.site.register(Cart)
class CartItemAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30">'.format(object.product.image.url))
    thumbnail.short_description = 'Product Image'
    # prepopulated_fields={'slug':('name',)}
    list_display=['thumbnail', 'user','product', 'cart', 'is_active']
    list_filter = ['is_active',]
    search_fields = ["user__email","product__name", "cart__cart_id"]
    list_display_links = ('user','product','cart',)
admin.site.register(CartItem, CartItemAdmin)