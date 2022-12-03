from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductOffers,DealsAndPromotions, Variation
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin
from django_admin_listfilter_dropdown.filters import DropdownFilter
# Register your models here.
class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    data_hierarchy = 'created_at'
    ordering = ('-modified_date',)
    list_display=('image_preview','name','price','stock','category','modified_date','is_available')
    prepopulated_fields={'slug':('name',)}
    search_fields = ["name","category__name"]
    list_display_links = ('name','category', 'image_preview',)
    readonly_fields = ['image_preview',]
    list_filter = [
        'is_available',
        ('category__name', DropdownFilter),
        'modified_date',
    ]
    def image_preview(self,obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;"/>'.format(obj.image.url))
        else:
            return mark_safe('<span>No Image Found</span>')

    

admin.site.register(Product,ProductAdmin)

class ProductOfferAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_display=('product','offer_name')
    search_fields = ["offer_name","product__name"]
    list_display_links = ('offer_name','product',)
    list_filter = [
        ('product__name', DropdownFilter),
    ]

admin.site.register(ProductOffers, ProductOfferAdmin)
class DealsAndPromotionsAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    def thumbnail(self, object):
        if object.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;"/>'.format(object.image.url))
        else:
            return mark_safe('<span>No Image Found</span>')
    readonly_fields = ['thumbnail',]
    thumbnail.short_description = 'Product Image'
    list_display=('thumbnail','product','discounted_price')
    search_fields = ["discounted_price","product__name"]
    list_display_links = ('product','thumbnail')
    list_filter = [
        ('product__name', DropdownFilter),
    ]

admin.site.register(DealsAndPromotions, DealsAndPromotionsAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_at',)
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active',)

admin.site.register(Variation, VariationAdmin)