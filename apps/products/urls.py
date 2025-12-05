# ========== apps/products/urls.py ==========
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, SpecialRequestViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('', ProductViewSet, basename='product')
router.register('special-requests', SpecialRequestViewSet, basename='special-request')

urlpatterns = [
    path('', include(router.urls)),
]