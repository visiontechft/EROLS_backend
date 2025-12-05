# ========== apps/products/models.py ==========
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    # Prix
    price_china = models.DecimalField(max_digits=10, decimal_places=2, help_text="Prix en Chine (FCFA)")
    price_cameroon = models.DecimalField(max_digits=10, decimal_places=2, help_text="Prix au Cameroun (FCFA)")
    
    # Stock et disponibilité
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    
    # Images
    main_image = models.ImageField(upload_to='products/')
    
    # Informations produit
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="Poids en kg")
    dimensions = models.CharField(max_length=100, blank=True, help_text="L x l x h en cm")
    
    # SEO et stats
    views_count = models.IntegerField(default=0)
    sales_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image {self.order} - {self.product.name}"

class SpecialRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('processing', 'En traitement'),
        ('quoted', 'Devis envoyé'),
        ('accepted', 'Accepté'),
        ('rejected', 'Rejeté'),
    )
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='special_requests')
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='special_requests/', blank=True, null=True)
    url_reference = models.URLField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    admin_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product_name} - {self.user.username}"