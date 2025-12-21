from rest_framework import serializers
from .models import City, Order
from apps.products.models import Product


class CitySerializer(serializers.ModelSerializer):
    """Serializer pour les villes disponibles"""
    class Meta:
        model = City
        fields = ['id', 'name', 'whatsapp_number', 'display_order']


class InitiateOrderSerializer(serializers.Serializer):
    """Serializer pour initier une commande (générer URL WhatsApp)"""
    product_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)
    
    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, is_available=True)
            if product.stock <= 0:
                raise serializers.ValidationError("Ce produit n'est plus en stock.")
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Produit introuvable ou non disponible.")
    
    def validate_city_id(self, value):
        try:
            City.objects.get(id=value, is_active=True)
            return value
        except City.DoesNotExist:
            raise serializers.ValidationError("Ville introuvable ou non disponible.")
    
    def validate(self, data):
        """Vérifier que la quantité ne dépasse pas le stock"""
        product = Product.objects.get(id=data['product_id'])
        quantity = data.get('quantity', 1)
        
        if quantity > product.stock:
            raise serializers.ValidationError(
                f"Stock insuffisant. Disponible: {product.stock}"
            )
        
        return data
    
    def create(self, validated_data):
        """Créer une entrée de commande et retourner l'URL WhatsApp"""
        product = Product.objects.get(id=validated_data['product_id'])
        city = City.objects.get(id=validated_data['city_id'])
        user = self.context['request'].user
        quantity = validated_data.get('quantity', 1)
        
        # Créer l'historique de commande
        order = Order.objects.create(
            user=user,
            product=product,
            city=city,
            product_name=product.name,
            product_price=product.price,
            city_name=city.name,
            whatsapp_number=city.whatsapp_number,
            quantity=quantity,
            status='redirected'
        )
        
        # Générer l'URL WhatsApp
        whatsapp_url = city.get_whatsapp_url(product, user, quantity)
        
        return {
            'order_id': order.id,
            'whatsapp_url': whatsapp_url,
            'city': city.name,
            'product': product.name,
            'price': product.price
        }


class InitiateCartOrderSerializer(serializers.Serializer):
    """Serializer pour initier une commande de panier (plusieurs produits)"""
    items = serializers.ListField(
        child=serializers.DictField(),
        min_length=1
    )
    city_id = serializers.IntegerField()
    
    def validate_items(self, value):
        """Valider chaque item du panier"""
        for item in value:
            if 'product_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError(
                    "Chaque item doit contenir 'product_id' et 'quantity'."
                )
            
            try:
                product_id = int(item['product_id'])
                quantity = int(item['quantity'])
            except (ValueError, TypeError):
                raise serializers.ValidationError(
                    "product_id et quantity doivent être des nombres."
                )
            
            if quantity <= 0:
                raise serializers.ValidationError("La quantité doit être supérieure à 0.")
            
            # Vérifier le produit
            try:
                product = Product.objects.get(id=product_id, is_available=True)
                if product.stock < quantity:
                    raise serializers.ValidationError(
                        f"Stock insuffisant pour {product.name}. Disponible: {product.stock}"
                    )
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f"Produit avec l'ID {product_id} introuvable ou non disponible."
                )
        
        return value
    
    def validate_city_id(self, value):
        try:
            City.objects.get(id=value, is_active=True)
            return value
        except City.DoesNotExist:
            raise serializers.ValidationError("Ville introuvable ou non disponible.")
    
    def create(self, validated_data):
        """Créer plusieurs commandes et retourner l'URL WhatsApp groupée"""
        items_data = validated_data['items']
        city = City.objects.get(id=validated_data['city_id'])
        user = self.context['request'].user
        
        order_ids = []
        total_price = 0
        products_text = []
        
        # Créer une commande pour chaque produit
        for item_data in items_data:
            product = Product.objects.get(id=int(item_data['product_id']))
            quantity = int(item_data['quantity'])
            
            # Créer l'ordre
            order = Order.objects.create(
                user=user,
                product=product,
                city=city,
                product_name=product.name,
                product_price=product.price,
                city_name=city.name,
                whatsapp_number=city.whatsapp_number,
                quantity=quantity,
                status='redirected'
            )
            
            order_ids.append(order.id)
            total_price += float(product.price) * quantity
            products_text.append(f"- {product.name} x{quantity} = {float(product.price) * quantity:,.0f} FCFA")
        
        # Générer l'URL WhatsApp groupée
        from urllib.parse import quote
        message = (
            f"Bonjour! Je souhaite commander:\n\n"
            f"{chr(10).join(products_text)}\n\n"
            f"*Total:* {total_price:,.0f} FCFA\n"
            f"*Client:* {user.get_full_name() or user.username}\n"
            f"*Ville:* {city.name}\n\n"
            f"Merci de me confirmer la disponibilité et les frais de livraison."
        )
        encoded_message = quote(message)
        whatsapp_url = f"https://wa.me/{city.whatsapp_number}?text={encoded_message}"
        
        return {
            'order_ids': order_ids,
            'whatsapp_url': whatsapp_url,
            'city': city.name,
            'items_count': len(items_data),
            'total_price': total_price
        }


class OrderHistorySerializer(serializers.ModelSerializer):
    """Serializer pour l'historique des commandes"""
    product_name = serializers.CharField()
    city_name = serializers.CharField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'product_name', 'product_price', 'quantity',
            'city_name', 'status', 'status_display',
            'created_at', 'updated_at'
        ]