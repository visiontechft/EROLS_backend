from django.db import models
from apps.users.models import User
from apps.products.models import Product


class City(models.Model):
    """Villes disponibles avec leurs numéros WhatsApp"""
    name = models.CharField(max_length=100, unique=True)
    whatsapp_number = models.CharField(max_length=20, help_text="Format: 237XXXXXXXXX (sans +)")
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Ville'
        verbose_name_plural = 'Villes'
    
    def __str__(self):
        return self.name
    
    def get_whatsapp_url(self, product, user, quantity=1):
        """Générer l'URL WhatsApp avec le message pré-rempli"""
        total = float(product.price) * quantity
        message = (
            f"Bonjour! Je suis intéressé(e) par:\n\n"
            f"*Produit:* {product.name}\n"
            f"*Prix unitaire:* {product.price:,.0f} FCFA\n"
            f"*Quantité:* {quantity}\n"
            f"*Total:* {total:,.0f} FCFA\n"
            f"*Client:* {user.get_full_name() or user.username}\n"
            f"*Ville:* {self.name}\n\n"
            f"Je souhaite commander ce produit."
        )
        # Encoder le message pour l'URL
        from urllib.parse import quote
        encoded_message = quote(message)
        return f"https://wa.me/{self.whatsapp_number}?text={encoded_message}"


class Order(models.Model):
    """Historique des commandes passées (pour tracking uniquement)"""
    STATUS_CHOICES = (
        ('redirected', 'Redirigé vers WhatsApp'),
        ('completed', 'Complétée'),
        ('cancelled', 'Annulée'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    
    # Snapshot des infos au moment de la redirection
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    city_name = models.CharField(max_length=100)
    whatsapp_number = models.CharField(max_length=20)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='redirected')
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
    
    def __str__(self):
        return f"{self.user.username} - {self.product_name} - {self.city_name}"