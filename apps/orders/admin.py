# ========== apps/orders/admin.py ==========
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'price', 'quantity', 'subtotal']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_status', 'total', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'delivery_phone']
    readonly_fields = ['order_number', 'subtotal', 'total', 'created_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'order_number', 'status', 'payment_status', 'payment_method')
        }),
        ('Livraison', {
            'fields': ('delivery_address', 'delivery_city', 'delivery_phone', 'estimated_delivery')
        }),
        ('Montants', {
            'fields': ('subtotal', 'shipping_cost', 'total')
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes')
        }),
    )