from django.contrib import admin
from .models import Category
from django.utils.html import format_html
# Register your models here.
class categoryAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.image:
            return format_html('<img src="{}" width="30">'.format(object.image.url))
        else:
            return 'No Image Found'
    thumbnail.short_description = 'Category Image'
    prepopulated_fields={'slug':('name',)}
    list_display=['thumbnail','name','slug']
    # list_display=('image','name', 'slug')
    search_fields = ["name","slug"]
    list_display_links = ('thumbnail','name','slug')
    list_per_page = 20
    
    fieldsets = (
    (None, {
        'classes': ('tab-general',),
        'fields' : ('image','name','slug') 
    }),
    )

    tabs = [
        ("General", ["tab-general"]),
    ]

admin.site.register(Category,categoryAdmin)
