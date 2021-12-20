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
    # list_display=('image','name', 'slug')
    search_fields = ["name","slug"]
    list_display_links = ('name','slug','thumbnail',)

admin.site.register(Category,categoryAdmin)
