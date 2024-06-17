from django.contrib import admin
from .models import User, Address
from django.contrib.admin.models import LogEntry

admin.site.register(LogEntry)

class UserAdmin(admin.ModelAdmin):
    list_display = ("id",'username', 'email', 'mobNo', 'profile_img', "is_active", 'is_superuser')
    search_fields = ('username', 'email', 'mobNo', 'is_active', 'is_superuser' )

admin.site.register(User, UserAdmin)


class UserAdd(admin.ModelAdmin):
    list_display = ("address_type", "street1", "street2", "city", "pincode", "user_id")
    search_fields = ("user_id", "city", "pincode","address_type")

admin.site.register(Address, UserAdd)


# from allauth.socialaccount.models import SocialApp
# from allauth.socialaccount.admin import SocialAppAdmin
# from django.contrib import admin

# admin.site.unregister(SocialApp)
# admin.site.register(SocialApp, SocialAppAdmin)