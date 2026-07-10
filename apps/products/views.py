from decimal import Decimal, InvalidOperation

from django.core.cache import cache
from django.db.models import OuterRef, Subquery
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .cache import TTL_DETAIL, TTL_MEDIUM, TTL_SHORT, bump_cache_version, versioned_key
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


def _featured_per_category_queryset():
    """One product per active category (most recent, in stock, with a photo),
    fetched in 2 queries total instead of 1-per-category (N+1)."""
    latest_id_per_category = (
        Product.objects
        .filter(category=OuterRef('pk'), is_available=True, stock__gt=0)
        .exclude(image='')
        .order_by('-created_at')
        .values('id')[:1]
    )
    category_ids = (
        Category.objects
        .filter(is_active=True)
        .annotate(featured_product_id=Subquery(latest_id_per_category))
        .exclude(featured_product_id=None)
        .values_list('featured_product_id', flat=True)
    )
    return (
        Product.objects
        .filter(id__in=list(category_ids))
        .select_related('category')
        .order_by('category__name')
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

    def list(self, request, *args, **kwargs):
        key = versioned_key('categories', 'list')
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)
        response = super().list(request, *args, **kwargs)
        cache.set(key, response.data, TTL_MEDIUM)
        return response

    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """Retourne tous les produits d'une catégorie"""
        category = self.get_object()
        products = category.products.filter(is_available=True).select_related('category')

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
    
    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get(self.lookup_url_kwarg or self.lookup_field)
        key = versioned_key('product', 'detail', slug)
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)
        response = super().retrieve(request, *args, **kwargs)
        cache.set(key, response.data, TTL_DETAIL)
        return response

    def _featured_queryset(self):
        return self.get_queryset().filter(stock__gt=0)[:8]

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Retourne les produits mis en avant (les plus récents avec stock)"""
        key = versioned_key('products', 'featured')
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)
        serializer = ProductListSerializer(self._featured_queryset(), many=True, context={'request': request})
        cache.set(key, serializer.data, TTL_SHORT)
        return Response(serializer.data)

    def _popular_queryset(self):
        # Pour l'instant, produits avec le moins de stock restant (proxy de vente
        # rapide) ; a remplacer par un vrai compteur de ventes des qu'il existe.
        return self.get_queryset().order_by('stock')[:8]

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Retourne les produits populaires (basé sur le stock vendu)"""
        key = versioned_key('products', 'popular')
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)
        serializer = ProductListSerializer(self._popular_queryset(), many=True, context={'request': request})
        cache.set(key, serializer.data, TTL_SHORT)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='featured-per-category')
    def featured_per_category(self, request):
        """Retourne un produit vedette (le plus recent, avec photo) par categorie active."""
        key = versioned_key('products', 'featured-per-category')
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)
        serializer = ProductListSerializer(
            _featured_per_category_queryset(), many=True, context={'request': request}
        )
        cache.set(key, serializer.data, TTL_SHORT)
        return Response(serializer.data)

    # Vraies marques presentes dans le catalogue (pas de "partenariat" invente) :
    # on ne montre que celles ayant au moins un produit reel en stock.
    KNOWN_BRANDS = [
        'OSCAR', 'HISENSE', 'MIDEA', 'INNOVA', 'TOBI', 'FODEG Star', 'GIFTMAX',
        'Sylver Crest', 'STAR-X', 'STARX', 'Light Wave', 'JBL', 'Grious', 'DORAGYM',
        'RMG', 'VISION', 'SAMSUNG', 'LG', 'SONAR', 'Hoffmans',
    ]

    def _brands_data(self, request):
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
        return results

    @action(detail=False, methods=['get'])
    def brands(self, request):
        """Retourne les marques reellement presentes dans le catalogue actuel,
        avec le nombre de produits et une photo representative."""
        key = versioned_key('products', 'brands')
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)
        data = self._brands_data(request)
        cache.set(key, data, TTL_MEDIUM)
        return Response(data)

    @action(detail=False, methods=['get'])
    def homepage(self, request):
        """Agrege en un seul appel tout ce dont la page d'accueil a besoin
        (featured, popular, vedette par categorie, categories, marques) —
        remplace 5 aller-retours reseau par 1 seul."""
        key = versioned_key('products', 'homepage')
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)

        ctx = {'request': request}
        data = {
            'featured': ProductListSerializer(self._featured_queryset(), many=True, context=ctx).data,
            'popular': ProductListSerializer(self._popular_queryset(), many=True, context=ctx).data,
            'featured_per_category': ProductListSerializer(
                _featured_per_category_queryset(), many=True, context=ctx
            ).data,
            'categories': CategorySerializer(
                Category.objects.filter(is_active=True), many=True, context=ctx
            ).data,
            'brands': self._brands_data(request),
        }
        cache.set(key, data, TTL_SHORT)
        return Response(data)

    @action(detail=True, methods=['get'])
    def related(self, request, slug=None):
        """Retourne des produits similaires (même catégorie)"""
        product = self.get_object()
        key = versioned_key('product', 'related', slug)
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)
        related_products = (
            Product.objects
            .filter(category=product.category, is_available=True)
            .select_related('category')
            .exclude(id=product.id)
            .order_by('?')[:4]  # 4 produits aléatoires
        )
        serializer = ProductListSerializer(related_products, many=True, context={'request': request})
        cache.set(key, serializer.data, TTL_SHORT)
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
        sur tous les produits, une seule catégorie, et/ou une tranche de prix
        (min_price/max_price, inclusifs) — utile pour appliquer un barème par palier."""
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

        min_price = request.data.get('min_price')
        if min_price not in (None, ''):
            try:
                queryset = queryset.filter(price__gte=Decimal(str(min_price)))
            except InvalidOperation:
                return Response({'error': 'min_price invalide'}, status=400)

        max_price = request.data.get('max_price')
        if max_price not in (None, ''):
            try:
                queryset = queryset.filter(price__lte=Decimal(str(max_price)))
            except InvalidOperation:
                return Response({'error': 'max_price invalide'}, status=400)

        # bulk_update() issues a small number of SQL statements instead of one
        # UPDATE per product (and per-product post_save signals) — individual
        # .save() calls over a few hundred products was slow enough to trip
        # the frontend's request timeout, leaving the run half-applied.
        to_update = []
        for product in queryset.only('id', 'price'):
            if mode == 'percent':
                new_price = product.price * (Decimal('1') + value / Decimal('100'))
            else:
                new_price = product.price + value
            product.price = max(new_price, Decimal('0')).quantize(Decimal('1'))
            to_update.append(product)

        Product.objects.bulk_update(to_update, ['price'], batch_size=200)
        if to_update:
            bump_cache_version()

        return Response({'updated': len(to_update)})

    @action(detail=False, methods=['post'], url_path='bulk-price-tiers')
    def bulk_price_tiers(self, request):
        """Applique un barème de paliers de prix en UNE SEULE passe : chaque
        produit est évalué une seule fois contre son prix ACTUEL (avant toute
        modification de cette requête) pour trouver son palier, puis reçoit le
        bonus correspondant, une seule fois.

        C'est le pendant sûr de bulk-price-update appelé palier par palier :
        appliquer les paliers un par un peut faire "changer de tranche" un
        produit après un ajustement (ex. 300F +300 -> 600F) et le faire
        re-matcher par le palier suivant (500-1499F) lors d'un appel séparé,
        doublant l'ajustement. Ici, tous les paliers sont fournis en une seule
        requête et chaque produit ne peut matcher qu'un seul palier (le premier
        dont l'intervalle le contient), donc aucun double ajustement possible.
        """
        tiers_data = request.data.get('tiers')
        if not isinstance(tiers_data, list) or not tiers_data:
            return Response({'error': 'tiers doit être une liste non vide'}, status=400)

        tiers = []
        for t in tiers_data:
            try:
                min_price = Decimal(str(t['min_price'])) if t.get('min_price') not in (None, '') else None
                max_price = Decimal(str(t['max_price'])) if t.get('max_price') not in (None, '') else None
                bonus = Decimal(str(t['bonus']))
            except (KeyError, TypeError, InvalidOperation):
                return Response({'error': 'palier invalide'}, status=400)
            tiers.append((min_price, max_price, bonus))

        queryset = Product.objects.all()
        category_id = request.data.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        to_update = []
        for product in queryset.only('id', 'price'):
            price = product.price
            for min_price, max_price, bonus in tiers:
                if (min_price is None or price >= min_price) and (max_price is None or price <= max_price):
                    product.price = max(price + bonus, Decimal('0')).quantize(Decimal('1'))
                    to_update.append(product)
                    break

        # bulk_update() in one/few SQL statements instead of one .save() per
        # product — the previous per-row loop was slow enough on ~300
        # products to trip the frontend's request timeout mid-run, leaving
        # some products bumped and others not.
        Product.objects.bulk_update(to_update, ['price'], batch_size=200)
        if to_update:
            bump_cache_version()

        return Response({'updated': len(to_update)})