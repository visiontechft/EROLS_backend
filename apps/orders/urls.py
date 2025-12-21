from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CityViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]

# Endpoints disponibles:
# GET    /api/cities/                 - Liste des villes
# POST   /api/orders/initiate/        - Initier une commande (obtenir URL WhatsApp)
# GET    /api/orders/history/         - Historique des commandes
# GET    /api/orders/stats/           - Statistiques
# PATCH  /api/orders/{id}/update_status/ - Mettre à jour le statut