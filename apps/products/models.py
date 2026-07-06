# apps/products/models.py
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Image stockée localement (media/products/)
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
    )
    
    # Disponibilité
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def in_stock(self):
        """Vérifie si le produit est en stock"""
        return self.stock > 0
    
    @property
    def image_url(self):
        """Retourne l'URL de l'image, ou None si aucune image (le frontend affiche un placeholder local)"""
        if self.image:
            return self.image.url
        return None
    
    def get_image_thumbnail(self, width=300, height=300):
        """Retourne l'URL de l'image (pas de redimensionnement côté serveur)"""
        return self.image_url


class ProductImage(models.Model):
    """Galerie d'images d'un produit (en plus de l'image principale)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} — image {self.order}"

    @property
    def image_url(self):
        return self.image.url if self.image else None