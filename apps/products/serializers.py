# ========== apps/products/serializers.py ==========
from rest_framework import serializers
from .models import Category, Product, ProductImage, SpecialRequest

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'parent', 'children', 'is_active']
    
    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.filter(is_active=True), many=True).data
        return []

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order']

class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'main_image', 'price_china', 'price_cameroon', 
                  'category_name', 'is_available', 'stock']

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

class SpecialRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = SpecialRequest
        fields = ['id', 'user', 'user_name', 'product_name', 'description', 'image', 
                  'url_reference', 'quantity', 'status', 'estimated_price', 'admin_notes', 'created_at']
        read_only_fields = ['user', 'status', 'estimated_price', 'admin_notes']

