from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    ProductListSerializer,
    ProductCreateUpdateSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les catégories (lecture seule)
    
    list: Retourne toutes les catégories actives
    retrieve: Retourne une catégorie spécifique avec ses produits
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """Retourne tous les produits d'une catégorie"""
        category = self.get_object()
        products = category.products.filter(is_available=True)
        
        # Filtrage optionnel
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les produits
    
    list: Retourne tous les produits disponibles avec pagination
    retrieve: Retourne les détails d'un produit
    create: Crée un nouveau produit (admin uniquement)
    update: Met à jour un produit (admin uniquement)
    delete: Supprime un produit (admin uniquement)
    """
    queryset = Product.objects.filter(is_available=True).select_related('category')
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'is_available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Utilise différents serializers selon l'action"""
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer
    
    def get_queryset(self):
        """Filtre personnalisé des produits"""
        queryset = super().get_queryset()
        
        # Filtrer par prix
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filtrer par disponibilité en stock
        in_stock_only = self.request.query_params.get('in_stock')
        if in_stock_only and in_stock_only.lower() == 'true':
            queryset = queryset.filter(stock__gt=0)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Retourne les produits mis en avant (les plus récents avec stock)"""
        products = self.get_queryset().filter(stock__gt=0)[:8]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Retourne les produits populaires (basé sur le stock vendu)"""
        # Pour l'instant, on retourne les produits avec le moins de stock
        # Plus tard, vous pourrez implémenter un système de comptage des ventes
        products = self.get_queryset().order_by('stock')[:8]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def related(self, request, slug=None):
        """Retourne des produits similaires (même catégorie)"""
        product = self.get_object()
        related_products = (
            Product.objects
            .filter(category=product.category, is_available=True)
            .exclude(id=product.id)
            .order_by('?')[:4]  # 4 produits aléatoires
        )
        serializer = ProductListSerializer(related_products, many=True, context={'request': request})
        return Response(serializer.data)