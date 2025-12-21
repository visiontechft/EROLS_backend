from django.contrib import admin
from django.utils.html import format_html
from .models import City, Order


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'whatsapp_number', 'is_active', 'display_order']
    list_filter = ['is_active']
    search_fields = ['name', 'whatsapp_number']
    list_editable = ['is_active', 'display_order']
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Informations de la ville', {
            'fields': ('name', 'whatsapp_number', 'is_active', 'display_order')
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'product_name', 'city_name', 
        'product_price_display', 'status_badge', 'created_at'
    ]
    list_filter = ['status', 'city_name', 'created_at']
    search_fields = ['user__username', 'user__email', 'product_name', 'city_name']
    readonly_fields = [
        'user', 'product', 'city', 'product_name', 
        'product_price', 'city_name', 'whatsapp_number', 
        'created_at', 'updated_at'
    ]
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Client', {
            'fields': ('user', 'created_at', 'updated_at')
        }),
        ('Commande', {
            'fields': ('product', 'product_name', 'product_price', 'status')
        }),
        ('Livraison', {
            'fields': ('city', 'city_name', 'whatsapp_number')
        }),
    )
    
    def status_badge(self, obj):
        """Badge coloré pour le statut"""
        colors = {
            'redirected': '#FFA500',  # Orange
            'completed': '#008000',   # Vert
            'cancelled': '#DC143C',   # Rouge
        }
        color = colors.get(obj.status, '#808080')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Statut'
    
    def product_price_display(self, obj):
        """Prix formaté"""
        return f"{obj.product_price:,.0f} FCFA"
    product_price_display.short_description = 'Prix'
    product_price_display.admin_order_field = 'product_price'
    
    def get_queryset(self, request):
        """Optimiser les requêtes"""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'product', 'city')
    
    actions = ['mark_as_completed', 'mark_as_cancelled']
    
    def mark_as_completed(self, request, queryset):
        """Marquer les commandes comme complétées"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} commande(s) marquée(s) comme complétée(s).')
    mark_as_completed.short_description = "Marquer comme complétée"
    
    def mark_as_cancelled(self, request, queryset):
        """Marquer les commandes comme annulées"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} commande(s) annulée(s).')
    mark_as_cancelled.short_description = "Marquer comme annulée"