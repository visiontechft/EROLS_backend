from rest_framework import serializers
from .models import Category, Product, ProductImage


def _absolute_image_url(obj, request):
    """Construit une URL absolue pour l'image (media local), sinon renvoie le placeholder"""
    if not obj.image:
        return obj.image_url
    return request.build_absolute_uri(obj.image.url) if request else obj.image.url


class ProductImageSerializer(serializers.ModelSerializer):
    """Une image de la galerie d'un produit"""
    url = serializers.SerializerMethodField()
    is_primary = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'url', 'alt_text', 'is_primary', 'order']

    def get_url(self, obj):
        return _absolute_image_url(obj, self.context.get('request'))

    def get_is_primary(self, obj):
        return obj.order == 0


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
        """Retourne l'URL complète de l'image"""
        return _absolute_image_url(obj, self.context.get('request'))

    def get_thumbnail_url(self, obj):
        """Retourne l'URL de l'image (pas de miniature dédiée)"""
        return _absolute_image_url(obj, self.context.get('request'))


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
    images = ProductImageSerializer(many=True, read_only=True)
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description',
            'price', 'stock', 'in_stock', 'is_available',
            'category', 'category_id',
            'image', 'image_url', 'thumbnail_url',
            'medium_image_url', 'large_image_url', 'images',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
        extra_kwargs = {
            'image': {'write_only': True}
        }
    
    def get_image_url(self, obj):
        """URL originale de l'image"""
        return _absolute_image_url(obj, self.context.get('request'))

    def get_thumbnail_url(self, obj):
        """Pas de miniature dédiée : renvoie l'image originale"""
        return _absolute_image_url(obj, self.context.get('request'))

    def get_medium_image_url(self, obj):
        """Pas de variante dédiée : renvoie l'image originale"""
        return _absolute_image_url(obj, self.context.get('request'))

    def get_large_image_url(self, obj):
        """Pas de variante dédiée : renvoie l'image originale"""
        return _absolute_image_url(obj, self.context.get('request'))


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