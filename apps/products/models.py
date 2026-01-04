# apps/products/models.py
from django.db import models
from cloudinary.models import CloudinaryField
from cloudinary import CloudinaryImage  # ← Ajoutez cette ligne


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
    
    # Image stockée sur Cloudinary
    image = CloudinaryField(
        'image',
        folder='products/',  # Dossier dans Cloudinary
        blank=True,
        null=True,
        transformation={
            'quality': 'auto',
            'fetch_format': 'auto'
        }
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
        """Retourne l'URL de l'image ou une image par défaut"""
        if self.image:
            return self.image.url
        return 'https://via.placeholder.com/400x400?text=No+Image'
    
    def get_image_thumbnail(self, width=300, height=300):
        """Génère une miniature de l'image"""
        if self.image:
            return CloudinaryImage(self.image.public_id).build_url(  # ← Utilisez CloudinaryImage directement
                width=width,
                height=height,
                crop='fill',
                quality='auto',
                fetch_format='auto'
            )
        return self.image_url