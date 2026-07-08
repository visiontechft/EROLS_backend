from decimal import Decimal, InvalidOperation

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Product, ProductImage
from .permissions import IsStaffOrReadOnly
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductListSerializer,
    ProductCreateUpdateSerializer,
    ProductImageSerializer,
    _absolute_image_url,
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
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    SORT_MAP = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name_asc': 'name',
        'name_desc': '-name',
        'newest': '-created_at',
    }

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

        # Filtrer par catégorie (slug)
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

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

        # Tri
        sort_by = self.request.query_params.get('sort_by')
        if sort_by in self.SORT_MAP:
            queryset = queryset.order_by(self.SORT_MAP[sort_by])

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
    
    @action(detail=False, methods=['get'], url_path='featured-per-category')
    def featured_per_category(self, request):
        """Retourne un produit vedette (le plus recent, avec photo) par categorie active."""
        results = []
        for category in Category.objects.filter(is_active=True).order_by('name'):
            product = (
                category.products
                .filter(is_available=True, stock__gt=0)
                .exclude(image='')
                .order_by('-created_at')
                .first()
            )
            if product:
                results.append(product)
        serializer = ProductListSerializer(results, many=True, context={'request': request})
        return Response(serializer.data)

    # Vraies marques presentes dans le catalogue (pas de "partenariat" invente) :
    # on ne montre que celles ayant au moins un produit reel en stock.
    KNOWN_BRANDS = [
        'OSCAR', 'HISENSE', 'MIDEA', 'INNOVA', 'TOBI', 'FODEG Star', 'GIFTMAX',
        'Sylver Crest', 'STAR-X', 'STARX', 'Light Wave', 'JBL', 'Grious', 'DORAGYM',
        'RMG', 'VISION', 'SAMSUNG', 'LG', 'SONAR', 'Hoffmans',
    ]

    @action(detail=False, methods=['get'])
    def brands(self, request):
        """Retourne les marques reellement presentes dans le catalogue actuel,
        avec le nombre de produits et une photo representative."""
        queryset = self.get_queryset()
        results = []
        seen_upper = set()
        for brand in self.KNOWN_BRANDS:
            key = brand.upper()
            if key in seen_upper:
                continue
            matches = queryset.filter(name__icontains=brand)
            count = matches.count()
            if count == 0:
                continue
            seen_upper.add(key)
            sample = matches.exclude(image='').first()
            results.append({
                'name': brand,
                'product_count': count,
                'image_url': _absolute_image_url(sample, request) if sample else None,
            })
        results.sort(key=lambda b: -b['product_count'])
        return Response(results)

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

    @action(detail=True, methods=['post'], url_path='images')
    def upload_images(self, request, slug=None):
        """Ajoute une ou plusieurs images à la galerie du produit"""
        product = self.get_object()
        files = request.FILES.getlist('images')
        if not files:
            return Response({'error': 'Aucune image fournie'}, status=400)

        start_order = product.images.count()
        created = [
            ProductImage.objects.create(product=product, image=f, order=start_order + i)
            for i, f in enumerate(files)
        ]
        serializer = ProductImageSerializer(created, many=True, context={'request': request})
        return Response(serializer.data, status=201)

    @action(detail=True, methods=['delete'], url_path=r'images/(?P<image_id>\d+)')
    def delete_image(self, request, slug=None, image_id=None):
        """Supprime une image de la galerie du produit"""
        product = self.get_object()
        deleted, _ = product.images.filter(id=image_id).delete()
        if not deleted:
            return Response({'error': 'Image introuvable'}, status=404)
        return Response(status=204)

    @action(detail=False, methods=['post'], url_path='bulk-price-update')
    def bulk_price_update(self, request):
        """Applique une marge sur les prix en masse (pourcentage ou montant fixe),
        sur tous les produits ou sur une seule catégorie."""
        mode = request.data.get('mode')
        if mode not in ('percent', 'fixed'):
            return Response({'error': 'mode doit être "percent" ou "fixed"'}, status=400)

        try:
            value = Decimal(str(request.data.get('value')))
        except (TypeError, InvalidOperation):
            return Response({'error': 'Valeur invalide'}, status=400)

        queryset = Product.objects.all()
        category_id = request.data.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        updated = 0
        for product in queryset:
            if mode == 'percent':
                new_price = product.price * (Decimal('1') + value / Decimal('100'))
            else:
                new_price = product.price + value
            product.price = max(new_price, Decimal('0')).quantize(Decimal('1'))
            product.save(update_fields=['price'])
            updated += 1

        return Response({'updated': updated})