from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductOffers,DealsAndPromotions, Variation
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30">'.format(object.image.url))
    thumbnail.short_description = 'Product Image'
    list_display=('thumbnail','name','price','stock','category','modified_date','is_available')
    prepopulated_fields={'slug':('name',)}
    search_fields = ["name","category__name"]
    list_display_links = ('name','category', 'thumbnail',)

admin.site.register(Product,ProductAdmin)

class ProductOfferAdmin(admin.ModelAdmin):
    list_display=('product','offer_name')
    search_fields = ["offer_name","product__name"]
    list_display_links = ('offer_name','product',)

admin.site.register(ProductOffers, ProductOfferAdmin)
class DealsAndPromotionsAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="60" height="20">'.format(object.image.url))
    thumbnail.short_description = 'Product Image'
    list_display=('thumbnail','product','discounted_price')
    search_fields = ["discounted_price","product__name"]
    list_display_links = ('product','thumbnail')

admin.site.register(DealsAndPromotions, DealsAndPromotionsAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_at',)
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active',)

admin.site.register(Variation, VariationAdmin)