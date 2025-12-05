# ========== apps/products/admin.py ==========
from django.contrib import admin
from .models import Category, Product, ProductImage, SpecialRequest

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'parent']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_china', 'price_cameroon', 'stock', 'is_available', 'sales_count']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    inlines = [ProductImageInline]

@admin.register(SpecialRequest)
class SpecialRequestAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'user', 'quantity', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['product_name', 'user__username']
