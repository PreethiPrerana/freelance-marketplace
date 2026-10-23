from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
@admin.register(User)
class CustomUserAdmin(UserAdmin):
 ordering=("email",)
 list_display=("email","username","role","is_staff")
 fieldsets=UserAdmin.fieldsets + (("Marketplace", {"fields":("role",)}),)
 add_fieldsets=UserAdmin.add_fieldsets + (("Marketplace", {"fields":("email","role")}),)
