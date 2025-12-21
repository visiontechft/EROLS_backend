from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPES = (
        ('client', 'Client'),
        ('reseller', 'Revendeur'),
        ('vendor', 'Fournisseur'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='client')
    phone = models.CharField(max_length=20, blank=True, null=True)  
    whatsapp = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, default='Douala')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    @property
    def full_name(self):
        """Retourne le nom complet ou username"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username