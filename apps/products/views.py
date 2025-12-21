from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les catégories
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les produits
    """
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Recherche de produits"""
        query = request.query_params.get('q', '')
        if not query:
            return Response([])
        
        products = self.queryset.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )[:20]
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        """Filtrage personnalisé"""
        queryset = super().get_queryset()
        
        # Filtrer par catégorie
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filtrer par prix
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Trier
        sort_by = self.request.query_params.get('sort_by')
        if sort_by:
            sort_mapping = {
                'price_asc': 'price',
                'price_desc': '-price',
                'name_asc': 'name',
                'name_desc': '-name',
                'newest': '-created_at',
            }
            order = sort_mapping.get(sort_by, '-created_at')
            queryset = queryset.order_by(order)
        
        return queryset