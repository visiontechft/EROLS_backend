# ========== apps/orders/serializers.py ==========
from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.serializers import ProductListSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'price', 'quantity', 'subtotal']
        read_only_fields = ['product_name', 'product_image', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user', 'user_name', 'status', 'status_display',
                  'payment_status', 'payment_method', 'delivery_address', 'delivery_city',
                  'delivery_phone', 'subtotal', 'shipping_cost', 'total', 'customer_notes',
                  'items', 'created_at', 'estimated_delivery']
        read_only_fields = ['user', 'order_number', 'subtotal', 'total', 'created_at']

class CreateOrderSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    delivery_address = serializers.CharField()
    delivery_city = serializers.CharField()
    delivery_phone = serializers.CharField()
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_METHOD)
    customer_notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("La commande doit contenir au moins un produit.")
        return value
    
    def create(self, validated_data):
        from apps.products.models import Product
        from decimal import Decimal
        
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # Créer la commande
        order = Order.objects.create(
            user=user,
            delivery_address=validated_data['delivery_address'],
            delivery_city=validated_data['delivery_city'],
            delivery_phone=validated_data['delivery_phone'],
            payment_method=validated_data['payment_method'],
            customer_notes=validated_data.get('customer_notes', ''),
            subtotal=0,
            shipping_cost=2000,  # Frais de livraison fixes
            total=0
        )
        
        # Créer les items
        subtotal = Decimal('0')
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            quantity = int(item_data['quantity'])
            
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                product_image=product.main_image.url if product.main_image else '',
                price=product.price_cameroon,
                quantity=quantity
            )
            
            subtotal += product.price_cameroon * quantity
            
            # Mettre à jour le stock
            product.stock -= quantity
            product.sales_count += quantity
            product.save()
        
        # Mettre à jour les totaux
        order.subtotal = subtotal
        order.total = subtotal + order.shipping_cost
        order.save()
        
        return order