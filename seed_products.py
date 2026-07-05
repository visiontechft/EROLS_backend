#!/usr/bin/env python
"""
Script de création de catégories et produits populaires avec images
pour les achats courants des Camerounais vers la Chine
"""
import os
import sys
import django
from django.utils.text import slugify

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import cloudinary.uploader
from apps.products.models import Category, Product

def upload_image_from_url(url):
    """Televerse une image sur Cloudinary depuis une URL distante"""
    try:
        result = cloudinary.uploader.upload(url, folder='products')
        return result.get('public_id')
    except Exception as e:
        print(f"  ⚠️  Erreur upload image: {e}")
        return None

def create_categories_and_products():
    """Créer les catégories et produits populaires avec images"""
    
    print("🚀 Création des catégories et produits avec images...")
    
    # ==========================================================
    # CATÉGORIE 1 : ÉLECTRONIQUE & SMARTPHONES
    # ==========================================================
    electronics, _ = Category.objects.get_or_create(
        slug='electronique-smartphones',
        defaults={
            'name': 'Électronique & Smartphones',
            'description': 'Téléphones portables, accessoires et gadgets électroniques',
            'is_active': True
        }
    )
    print(f"✅ Catégorie créée: {electronics.name}")
    
    # Produits pour Électronique avec URLs d'images
    products_electronics = [
        {
            'name': 'Smartphone Android 6.5" 128GB',
            'description': 'Smartphone Android dernière génération, écran 6.5 pouces, 128GB de stockage, double SIM, caméra 48MP. Parfait pour tous vos besoins quotidiens.',
            'price': 75000,
            'stock': 50,
            'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800'
        },
        {
            'name': 'Écouteurs Bluetooth Sans Fil',
            'description': 'Écouteurs Bluetooth 5.0 avec boîtier de charge, autonomie 24h, qualité sonore premium, résistants à l\'eau.',
            'price': 8500,
            'stock': 100,
            'image_url': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800'
        },
        {
            'name': 'Power Bank 20000mAh',
            'description': 'Batterie externe haute capacité 20000mAh, charge rapide, 2 ports USB, compatible tous smartphones.',
            'price': 12000,
            'stock': 75,
            'image_url': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=800'
        }
    ]
    
    for product_data in products_electronics:
        image_url = product_data.pop('image_url', None)
        product, created = Product.objects.get_or_create(
            slug=slugify(product_data['name']),
            defaults={
                **product_data,
                'category': electronics,
                'is_available': True
            }
        )
        
        if created or not product.image:
            if image_url:
                public_id = upload_image_from_url(image_url)
                if public_id:
                    product.image = public_id
                    product.save()
                    print(f"  ✓ Produit créé avec image: {product.name}")
                else:
                    print(f"  ✓ Produit créé sans image: {product.name}")
            else:
                print(f"  ✓ Produit créé: {product.name}")

    # ==========================================================
    # CATÉGORIE 2 : MODE & VÊTEMENTS
    # ==========================================================
    fashion, _ = Category.objects.get_or_create(
        slug='mode-vetements',
        defaults={
            'name': 'Mode & Vêtements',
            'description': 'Vêtements, chaussures et accessoires de mode',
            'is_active': True
        }
    )
    print(f"✅ Catégorie créée: {fashion.name}")
    
    products_fashion = [
        {
            'name': 'Ensemble Africain Homme Brodé',
            'description': 'Ensemble traditionnel africain pour homme, broderie de qualité, tissu léger et respirant. Disponible en plusieurs tailles et couleurs.',
            'price': 25000,
            'stock': 40,
            'image_url': 'https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=800'
        },
        {
            'name': 'Baskets Sport Homme/Femme',
            'description': 'Baskets confortables pour sport et décontracté, semelle antidérapante, design moderne. Du 38 au 45.',
            'price': 18000,
            'stock': 60,
            'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800'
        },
        {
            'name': 'Sac à Main Femme Cuir',
            'description': 'Sac à main élégant en similicuir de qualité, plusieurs compartiments, bandoulière ajustable.',
            'price': 15000,
            'stock': 35,
            'image_url': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800'
        }
    ]
    
    for product_data in products_fashion:
        image_url = product_data.pop('image_url', None)
        product, created = Product.objects.get_or_create(
            slug=slugify(product_data['name']),
            defaults={
                **product_data,
                'category': fashion,
                'is_available': True
            }
        )
        
        if created or not product.image:
            if image_url:
                public_id = upload_image_from_url(image_url)
                if public_id:
                    product.image = public_id
                    product.save()
                    print(f"  ✓ Produit créé avec image: {product.name}")
                else:
                    print(f"  ✓ Produit créé sans image: {product.name}")

    # ==========================================================
    # CATÉGORIE 3 : MAISON & ÉLECTROMÉNAGER
    # ==========================================================
    home, _ = Category.objects.get_or_create(
        slug='maison-electromenager',
        defaults={
            'name': 'Maison & Électroménager',
            'description': 'Appareils électroménagers et articles pour la maison',
            'is_active': True
        }
    )
    print(f"✅ Catégorie créée: {home.name}")
    
    products_home = [
        {
            'name': 'Ventilateur Sur Pied 18 Pouces',
            'description': 'Ventilateur puissant sur pied, 3 vitesses, oscillation 90°, hauteur réglable, silencieux.',
            'price': 22000,
            'stock': 30,
            'image_url': 'https://images.unsplash.com/photo-1616627781431-711bde1450a1?w=800'
        },
        {
            'name': 'Mixer Blender 5 en 1',
            'description': 'Mixeur multifonction 5 en 1, moteur 500W, capacité 1.5L, lames en acier inoxydable.',
            'price': 18000,
            'stock': 25,
            'image_url': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=800'
        },
        {
            'name': 'Fer à Repasser à Vapeur',
            'description': 'Fer à repasser professionnel avec vapeur, semelle antiadhésive, température réglable.',
            'price': 12000,
            'stock': 45,
            'image_url': 'https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=800'
        }
    ]
    
    for product_data in products_home:
        image_url = product_data.pop('image_url', None)
        product, created = Product.objects.get_or_create(
            slug=slugify(product_data['name']),
            defaults={
                **product_data,
                'category': home,
                'is_available': True
            }
        )
        
        if created or not product.image:
            if image_url:
                public_id = upload_image_from_url(image_url)
                if public_id:
                    product.image = public_id
                    product.save()
                    print(f"  ✓ Produit créé avec image: {product.name}")

    # ==========================================================
    # CATÉGORIE 4 : BEAUTÉ & SOINS
    # ==========================================================
    beauty, _ = Category.objects.get_or_create(
        slug='beaute-soins',
        defaults={
            'name': 'Beauté & Soins',
            'description': 'Produits de beauté, cosmétiques et soins personnels',
            'is_active': True
        }
    )
    print(f"✅ Catégorie créée: {beauty.name}")
    
    products_beauty = [
        {
            'name': 'Kit Maquillage Professionnel 24 Pièces',
            'description': 'Kit complet de maquillage professionnel avec pinceaux, ombres à paupières, rouges à lèvres et plus.',
            'price': 28000,
            'stock': 20,
            'image_url': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800'
        },
        {
            'name': 'Sèche-Cheveux Ionique 2200W',
            'description': 'Sèche-cheveux professionnel avec technologie ionique, 3 températures, 2 vitesses, diffuseur inclus.',
            'price': 15000,
            'stock': 40,
            'image_url': 'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=800'
        },
        {
            'name': 'Set Manucure Pédicure Électrique',
            'description': 'Kit manucure/pédicure électrique avec 6 embouts, rechargeable, idéal pour soins des ongles.',
            'price': 9500,
            'stock': 55,
            'image_url': 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=800'
        }
    ]
    
    for product_data in products_beauty:
        image_url = product_data.pop('image_url', None)
        product, created = Product.objects.get_or_create(
            slug=slugify(product_data['name']),
            defaults={
                **product_data,
                'category': beauty,
                'is_available': True
            }
        )
        
        if created or not product.image:
            if image_url:
                public_id = upload_image_from_url(image_url)
                if public_id:
                    product.image = public_id
                    product.save()
                    print(f"  ✓ Produit créé avec image: {product.name}")

    # ==========================================================
    # CATÉGORIE 5 : JOUETS & ENFANTS
    # ==========================================================
    toys, _ = Category.objects.get_or_create(
        slug='jouets-enfants',
        defaults={
            'name': 'Jouets & Enfants',
            'description': 'Jouets éducatifs, jeux et articles pour enfants',
            'is_active': True
        }
    )
    print(f"✅ Catégorie créée: {toys.name}")
    
    products_toys = [
        {
            'name': 'Voiture Télécommandée 4x4',
            'description': 'Voiture RC 4x4 tout-terrain, batterie rechargeable, portée 50m, résistante aux chocs.',
            'price': 16000,
            'stock': 30,
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800'
        },
        {
            'name': 'Tablette Éducative Enfant',
            'description': 'Tablette éducative 7 pouces pour enfants, applications pré-installées, contrôle parental, écran protégé.',
            'price': 35000,
            'stock': 25,
            'image_url': 'https://images.unsplash.com/photo-1544816565-aa6a4754e5c9?w=800'
        },
        {
            'name': 'Set Construction 500 Pièces',
            'description': 'Jeu de construction éducatif 500 pièces, développe créativité et motricité, compatible avec grandes marques.',
            'price': 12500,
            'stock': 45,
            'image_url': 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=800'
        }
    ]
    
    for product_data in products_toys:
        image_url = product_data.pop('image_url', None)
        product, created = Product.objects.get_or_create(
            slug=slugify(product_data['name']),
            defaults={
                **product_data,
                'category': toys,
                'is_available': True
            }
        )
        
        if created or not product.image:
            if image_url:
                public_id = upload_image_from_url(image_url)
                if public_id:
                    product.image = public_id
                    product.save()
                    print(f"  ✓ Produit créé avec image: {product.name}")

    # ==========================================================
    # STATISTIQUES FINALES
    # ==========================================================
    print("\n" + "="*60)
    print("📊 STATISTIQUES FINALES")
    print("="*60)
    print(f"✅ Catégories créées: {Category.objects.count()}")
    print(f"✅ Produits créés: {Product.objects.count()}")
    products_with_images = Product.objects.exclude(image='').exclude(image=None).count()
    print(f"🖼️  Produits avec images: {products_with_images}")
    print("\n📋 Détails par catégorie:")
    for category in Category.objects.all():
        count = category.products.count()
        with_img = category.products.exclude(image='').exclude(image=None).count()
        print(f"  • {category.name}: {count} produit(s) ({with_img} avec image)")
    print("="*60)
    print("✅ Import terminé avec succès!")

if __name__ == '__main__':
    try:
        create_categories_and_products()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)