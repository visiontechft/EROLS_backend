# ========== apps/users/admin.py ==========
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'phone', 'user_type', 'is_verified', 'created_at']
    list_filter = ['user_type', 'is_verified', 'created_at']
    search_fields = ['username', 'email', 'phone']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Infos supplémentaires', {'fields': ('user_type', 'phone', 'whatsapp', 'address', 'city', 'is_verified')}),
    )