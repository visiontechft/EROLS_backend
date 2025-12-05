# ========== apps/products/views.py ==========
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, SpecialRequest
from .serializers import (CategorySerializer, ProductListSerializer, 
                          ProductDetailSerializer, SpecialRequestSerializer)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True, parent=None)
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_available=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'category__parent']
    search_fields = ['name', 'description']
    ordering_fields = ['price_cameroon', 'created_at', 'sales_count']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = self.queryset.order_by('-sales_count')[:10]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def best_sellers(self, request):
        best_sellers = self.queryset.order_by('-sales_count')[:20]
        serializer = self.get_serializer(best_sellers, many=True)
        return Response(serializer.data)

class SpecialRequestViewSet(viewsets.ModelViewSet):
    serializer_class = SpecialRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SpecialRequest.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)