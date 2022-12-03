from django.contrib import admin
from .models import Category
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
class categoryAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.image:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 300px;">'.format(object.image.url))
        else:
            return 'No Image Found'
    thumbnail.short_description = 'Category Image'
    prepopulated_fields={'slug':('name',)}
    list_display=['thumbnail','name','slug']
    # list_display=('image','name', 'slug')
    search_fields = ["name","slug"]
    list_display_links = ('thumbnail','name','slug')
    list_per_page = 20
    readonly_fields = ['thumbnail',]

    search_fields = ['name','slug']

admin.site.register(Category,categoryAdmin)
