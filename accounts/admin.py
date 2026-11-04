from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات اختصاصی', {'fields': ('phone_number', 'role')}),
    )
    list_display = ('username', 'phone_number', 'first_name', 'last_name', 'role', 'is_staff')