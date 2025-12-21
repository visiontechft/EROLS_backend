from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'product_count_display', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    
    def product_count_display(self, obj):
        """Affiche le nombre de produits actifs dans la catégorie"""
        count = obj.products.filter(is_available=True).count()
        return f"{count} produit{'s' if count > 1 else ''}"
    product_count_display.short_description = "Produits"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_available']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Prix et Stock', {
            'fields': ('price', 'stock', 'is_available')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiser les requêtes"""
        qs = super().get_queryset(request)
        return qs.select_related('category')