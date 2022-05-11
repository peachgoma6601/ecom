from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

class MyAccountAdmin(UserAdmin):
    list_display = ('email','username','last_login','date_joined','is_active')
    list_display_links = ('username','email')
    readonly_fields = ('last_login','date_joined')

    filter_horizontal =()
    list_filter = ()
    fieldsets =()

admin.site.register(Account,MyAccountAdmin)