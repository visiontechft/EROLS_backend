from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="EROLS EasyBuy API",
        default_version='v1',
        description="API pour la plateforme EROLS EasyBuy - Plateforme e-commerce camerounaise",
        terms_of_service="https://www.erols.cm/terms/",
        contact=openapi.Contact(email="contact@erols.cm"),
        license=openapi.License(name="Proprietary"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Administration Django
    path('admin/', admin.site.urls),
    
    # API REST Framework - Authentification browsable (requis pour Swagger)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Documentation API
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API Endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/orders/', include('apps.orders.urls')),
    # path('api/delivery/', include('apps.delivery.urls')),
    # path('api/marketplace/', include('apps.marketplace.urls')),
    # path('api/notifications/', include('apps.notifications.urls')),
]

# Servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)