from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'username', 'email', 'phone', 'full_name',
        'user_type_badge', 'is_verified_badge', 
        'is_active', 'created_at'
    ]
    list_filter = ['user_type', 'is_verified', 'is_active', 'created_at', 'city']
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': (
                'user_type', 'phone', 'whatsapp', 
                'address', 'city', 'is_verified'
            )
        }),
        ('Dates importantes', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': (
                'email', 'phone', 'user_type', 
                'whatsapp', 'city'
            )
        }),
    )
    
    def user_type_badge(self, obj):
        """Afficher un badge coloré pour le type d'utilisateur"""
        colors = {
            'client': '#3498db',      # Bleu
            'reseller': '#9b59b6',    # Violet
            'vendor': '#e74c3c',      # Rouge
        }
        color = colors.get(obj.user_type, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_user_type_display()
        )
    user_type_badge.short_description = 'Type'
    user_type_badge.admin_order_field = 'user_type'
    
    def is_verified_badge(self, obj):
        """Afficher un badge pour le statut de vérification"""
        if obj.is_verified:
            return format_html(
                '<span style="background-color: #27ae60; color: white; padding: 3px 10px; '
                'border-radius: 3px; font-weight: bold;">✓ Vérifié</span>'
            )
        return format_html(
            '<span style="background-color: #e67e22; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">✗ Non vérifié</span>'
        )
    is_verified_badge.short_description = 'Vérification'
    is_verified_badge.admin_order_field = 'is_verified'
    
    def get_queryset(self, request):
        """Optimiser les requêtes"""
        qs = super().get_queryset(request)
        return qs
    
    actions = ['verify_users', 'unverify_users', 'activate_users', 'deactivate_users']
    
    def verify_users(self, request, queryset):
        """Action pour vérifier les utilisateurs"""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} utilisateur(s) vérifié(s).')
    verify_users.short_description = "Marquer comme vérifié"
    
    def unverify_users(self, request, queryset):
        """Action pour retirer la vérification"""
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} utilisateur(s) non vérifié(s).')
    unverify_users.short_description = "Retirer la vérification"
    
    def activate_users(self, request, queryset):
        """Action pour activer les utilisateurs"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} utilisateur(s) activé(s).')
    activate_users.short_description = "Activer les comptes"
    
    def deactivate_users(self, request, queryset):
        """Action pour désactiver les utilisateurs"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} utilisateur(s) désactivé(s).')
    deactivate_users.short_description = "Désactiver les comptes"