from django.contrib import admin
from .models import Category
from django.utils.html import format_html
# Register your models here.
class categoryAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30">'.format(object.image.url))
    thumbnail.short_description = 'Category Image'
    prepopulated_fields={'slug':('name',)}
    list_display=['thumbnail', 'name','slug']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Category,categoryAdmin)
