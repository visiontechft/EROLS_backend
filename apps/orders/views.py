from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import City, Order
from .serializers import CitySerializer, InitiateOrderSerializer, OrderHistorySerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les villes disponibles
    
    Endpoints:
    - GET /api/cities/ : Liste des villes actives
    """
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    queryset = City.objects.filter(is_active=True)


class OrderViewSet(viewsets.GenericViewSet):
    """
    ViewSet pour la gestion des commandes
    
    Endpoints:
    - POST /api/orders/initiate/ : Initier une commande (obtenir URL WhatsApp)
    - GET /api/orders/history/ : Historique des commandes
    - GET /api/orders/stats/ : Statistiques
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def initiate(self, request):
        """
        Initier une commande et obtenir l'URL WhatsApp
        
        Body:
        {
            "product_id": 1,
            "city_id": 2,
            "quantity": 1  (optionnel, défaut: 1)
        }
        
        Response:
        {
            "order_id": 123,
            "whatsapp_url": "https://wa.me/237XXXXXXXXX?text=...",
            "city": "Douala",
            "product": "iPhone 15",
            "price": 500000
        }
        """
        serializer = InitiateOrderSerializer(
            data=request.data, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        
        return Response(result, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def initiate_cart(self, request):
        """
        Initier une commande pour plusieurs produits (panier)
        
        Body:
        {
            "items": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 3, "quantity": 1}
            ],
            "city_id": 2
        }
        
        Response:
        {
            "order_ids": [123, 124],
            "whatsapp_url": "https://wa.me/237XXXXXXXXX?text=...",
            "city": "Douala",
            "items_count": 2,
            "total_price": 750000
        }
        """
        from .serializers import InitiateCartOrderSerializer
        
        serializer = InitiateCartOrderSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        
        return Response(result, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Historique des commandes de l'utilisateur"""
        orders = self.get_queryset().order_by('-created_at')
        
        # Pagination optionnelle
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderHistorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = OrderHistorySerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des commandes"""
        orders = self.get_queryset()
        
        stats = {
            'total_orders': orders.count(),
            'redirected': orders.filter(status='redirected').count(),
            'completed': orders.filter(status='completed').count(),
            'cancelled': orders.filter(status='cancelled').count(),
        }
        
        return Response(stats)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Mettre à jour le statut d'une commande (pour l'admin via l'app)
        
        Body:
        {
            "status": "completed"  // ou "cancelled"
        }
        """
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in ['completed', 'cancelled']:
            return Response(
                {'error': 'Statut invalide. Utilisez "completed" ou "cancelled".'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = new_status
        order.save(update_fields=['status', 'updated_at'])
        
        serializer = OrderHistorySerializer(order)
        return Response(serializer.data)