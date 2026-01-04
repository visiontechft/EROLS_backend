from django.contrib import admin
from django.utils.html import format_html
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
    list_display = ['image_thumbnail', 'name', 'category', 'price', 'stock', 'is_available', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_available']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Prix et Stock', {
            'fields': ('price', 'stock', 'is_available')
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
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
    
    def image_thumbnail(self, obj):
        """Affiche une miniature dans la liste"""
        if obj.image:
            thumbnail_url = obj.get_image_thumbnail(width=50, height=50)
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                thumbnail_url
            )
        return format_html('<span style="color: #999;">Pas d\'image</span>')
    
    image_thumbnail.short_description = ''
    
    def image_preview(self, obj):
        """Affiche un aperçu de l'image dans le formulaire"""
        if obj.image:
            preview_url = obj.get_image_thumbnail(width=400, height=400)
            return format_html(
                '''
                <div style="margin-top: 10px;">
                    <img src="{}" style="max-width: 400px; max-height: 400px; border: 1px solid #ddd; border-radius: 4px; padding: 5px;" />
                    <p style="margin-top: 10px; color: #666;">
                        <strong>URL Cloudinary:</strong><br/>
                        <a href="{}" target="_blank" style="word-break: break-all;">{}</a>
                    </p>
                </div>
                ''',
                preview_url,
                obj.image.url,
                obj.image.url
            )
        return format_html('<p style="color: #999;">Aucune image uploadée</p>')
    
    image_preview.short_description = 'Aperçu de l\'image'
    
    class Media:
        css = {
            'all': ('admin/css/products_admin.css',)
        }