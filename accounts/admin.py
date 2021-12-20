from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'phone_number','last_login', 'date_joined', 'is_active')
    list_display_links = ('email','full_name')
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ["email","full_name", 'phone_number']
    ordering = ('-date_joined',)
    list_filter = ['is_active',]
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'contact_no', 'address_line', 'province', 'city', 'district')
    list_display_links = ('user','contact_no', 'thumbnail')
    search_fields = ["user__email","contact_no", 'address_line', 'province', 'city', 'district']

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)