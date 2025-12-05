# ========== apps/orders/views.py ==========
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        
        if order.status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'Cette commande ne peut plus être annulée.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'cancelled'
        order.save()
        
        # Restaurer le stock
        for item in order.items.all():
            if item.product:
                item.product.stock += item.quantity
                item.product.sales_count -= item.quantity
                item.product.save()
        
        return Response(OrderSerializer(order).data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        orders = self.get_queryset()
        return Response({
            'total_orders': orders.count(),
            'pending': orders.filter(status='pending').count(),
            'in_transit': orders.filter(status__in=['shipped', 'in_transit']).count(),
            'delivered': orders.filter(status='delivered').count(),
        })
