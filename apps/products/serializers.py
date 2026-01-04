from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'product_count']
    
    def get_product_count(self, obj):
        return obj.products.filter(is_available=True).count()


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour les listes de produits"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 
            'price', 'image_url', 'thumbnail_url',
            'stock', 'in_stock', 'is_available',
            'category_name'
        ]
    
    def get_image_url(self, obj):
        """Retourne l'URL complète de l'image depuis Cloudinary"""
        return obj.image_url
    
    def get_thumbnail_url(self, obj):
        """Retourne l'URL d'une miniature optimisée"""
        return obj.get_image_thumbnail(width=300, height=300)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer complet pour les détails de produit"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    medium_image_url = serializers.SerializerMethodField()
    large_image_url = serializers.SerializerMethodField()
    in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 
            'price', 'stock', 'in_stock', 'is_available',
            'category', 'category_id',
            'image', 'image_url', 'thumbnail_url', 
            'medium_image_url', 'large_image_url',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
        extra_kwargs = {
            'image': {'write_only': True}
        }
    
    def get_image_url(self, obj):
        """URL originale de l'image"""
        return obj.image_url
    
    def get_thumbnail_url(self, obj):
        """Miniature 300x300 pour les vignettes"""
        return obj.get_image_thumbnail(width=300, height=300)
    
    def get_medium_image_url(self, obj):
        """Image moyenne 600x600 pour les galeries"""
        return obj.get_image_thumbnail(width=600, height=600)
    
    def get_large_image_url(self, obj):
        """Grande image 1200x1200 pour les détails"""
        return obj.get_image_thumbnail(width=1200, height=1200)


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour créer/modifier des produits"""
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description',
            'category', 'price', 'stock', 'is_available',
            'image'
        ]
        read_only_fields = ['slug']
    
    def validate_price(self, value):
        """Valide que le prix est positif"""
        if value <= 0:
            raise serializers.ValidationError("Le prix doit être supérieur à 0")
        return value
    
    def validate_stock(self, value):
        """Valide que le stock est positif ou nul"""
        if value < 0:
            raise serializers.ValidationError("Le stock ne peut pas être négatif")
        return value