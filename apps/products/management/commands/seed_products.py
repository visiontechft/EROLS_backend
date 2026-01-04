from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.db.models import Avg
from apps.products.models import Category, Product


class Command(BaseCommand):
    help = 'Créer des catégories et produits de démonstration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            type=str,
            help='Nom de la catégorie à créer (electronique, mode, maison, toutes)',
            default='electronique'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Supprimer tous les produits existants avant de créer'
        )

    def handle(self, *args, **options):
        category_choice = options['category'].lower()
        clear = options['clear']

        if clear:
            self.stdout.write(self.style.WARNING('🗑️  Suppression des données existantes...'))
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Données supprimées'))

        # Données des catégories et produits
        categories_data = {
            'electronique': {
                'name': 'Électronique',
                'slug': 'electronique',
                'description': 'Produits électroniques populaires et tendances',
                'products': [
                    {
                        'name': 'Écouteurs Sans Fil Bluetooth',
                        'description': '''Écouteurs Bluetooth TWS avec boîtier de charge.
- Autonomie : 4-6 heures
- Bluetooth 5.0
- Son stéréo HD
- Résistant à l'eau (IPX4)
- Compatible iOS et Android
Parfait pour le sport et les appels.''',
                        'price': 5000,
                        'stock': 50
                    },
                    {
                        'name': 'Montre Connectée Smartwatch',
                        'description': '''Montre intelligente multifonctions.
- Écran tactile HD
- Suivi santé (fréquence cardiaque, sommeil)
- Notifications smartphone
- Autonomie 5-7 jours
- Étanche IP67
- Multiples cadrans
Idéale pour fitness et lifestyle.''',
                        'price': 8500,
                        'stock': 35
                    },
                    {
                        'name': 'Chargeur Rapide USB Type-C 20W',
                        'description': '''Chargeur rapide universel avec câble.
- Charge rapide 20W
- Compatible iPhone, Samsung, Xiaomi
- Protection surcharge
- Câble Type-C 1m inclus
- Compact et portable
Charge votre téléphone à 50% en 30 minutes.''',
                        'price': 3500,
                        'stock': 80
                    },
                    {
                        'name': 'Batterie Externe Power Bank 20000mAh',
                        'description': '''Power bank haute capacité ultra-portable.
- Capacité : 20000mAh
- 2 ports USB + 1 Type-C
- Charge rapide bidirectionnelle
- Affichage LED du niveau
- Léger et compact
Recharge votre téléphone 4-5 fois.''',
                        'price': 7000,
                        'stock': 45
                    },
                    {
                        'name': 'Lampe LED Anneau pour Selfie et Vidéo',
                        'description': '''Anneau lumineux professionnel pour photos et vidéos.
- 10 pouces avec trépied
- 3 modes d'éclairage (chaud, froid, naturel)
- 10 niveaux de luminosité
- Support téléphone inclus
- USB rechargeable
Parfait pour TikTok, Instagram, YouTube.''',
                        'price': 6500,
                        'stock': 30
                    }
                ]
            },
            'mode': {
                'name': 'Mode et Accessoires',
                'slug': 'mode-accessoires',
                'description': 'Accessoires de mode tendance',
                'products': [
                    {
                        'name': 'Sac à Dos USB Anti-Vol',
                        'description': 'Sac à dos moderne avec port USB de charge et compartiments anti-vol.',
                        'price': 12000,
                        'stock': 25
                    },
                    {
                        'name': 'Lunettes de Soleil Polarisées',
                        'description': 'Lunettes UV400 protection, style moderne et élégant.',
                        'price': 4500,
                        'stock': 40
                    },
                    {
                        'name': 'Montre Fashion Homme/Femme',
                        'description': 'Montre élégante avec bracelet en cuir ou métal.',
                        'price': 6000,
                        'stock': 50
                    },
                    {
                        'name': 'Ceinture en Cuir Automatique',
                        'description': 'Ceinture automatique de qualité, ajustement facile.',
                        'price': 5500,
                        'stock': 30
                    },
                    {
                        'name': 'Portefeuille RFID Protection',
                        'description': 'Portefeuille slim avec protection contre le vol de données.',
                        'price': 4000,
                        'stock': 45
                    }
                ]
            },
            'maison': {
                'name': 'Maison et Cuisine',
                'slug': 'maison-cuisine',
                'description': 'Articles pour la maison et la cuisine',
                'products': [
                    {
                        'name': 'Blender Portable USB Rechargeable',
                        'description': 'Mini blender portable pour smoothies et jus partout.',
                        'price': 8000,
                        'stock': 20
                    },
                    {
                        'name': 'Lampe LED Solaire Extérieur',
                        'description': 'Lampe solaire étanche pour jardin et terrasse.',
                        'price': 6500,
                        'stock': 35
                    },
                    {
                        'name': 'Organiseur Maquillage Rotatif',
                        'description': 'Organiseur rotatif 360° pour maquillage et cosmétiques.',
                        'price': 5000,
                        'stock': 40
                    },
                    {
                        'name': 'Balance de Cuisine Digitale',
                        'description': 'Balance précise jusqu\'à 5kg avec écran LCD.',
                        'price': 4500,
                        'stock': 30
                    },
                    {
                        'name': 'Distributeur Savon Automatique',
                        'description': 'Distributeur automatique sans contact, USB rechargeable.',
                        'price': 7000,
                        'stock': 25
                    }
                ]
            }
        }

        # Déterminer quelles catégories créer
        if category_choice == 'toutes':
            categories_to_create = categories_data.keys()
        elif category_choice in categories_data:
            categories_to_create = [category_choice]
        else:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Catégorie inconnue: {category_choice}. '
                    f'Utilisez: electronique, mode, maison, ou toutes'
                )
            )
            return

        # Créer les catégories et produits
        total_products = 0
        for cat_key in categories_to_create:
            cat_data = categories_data[cat_key]
            
            # Créer la catégorie
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'is_active': True
                }
            )
            
            status = '✅ créée' if created else '🔄 existante'
            self.stdout.write(f"\n{status} Catégorie : {self.style.SUCCESS(category.name)}")
            
            # Créer les produits
            for product_data in cat_data['products']:
                slug = slugify(product_data['name'])
                product, created = Product.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'name': product_data['name'],
                        'description': product_data['description'],
                        'category': category,
                        'price': product_data['price'],
                        'stock': product_data['stock'],
                        'is_available': True
                    }
                )
                
                status_icon = '✅' if created else '🔄'
                self.stdout.write(
                    f"  {status_icon} {product.name} - "
                    f"{self.style.SUCCESS(f'{product.price:,.0f} FCFA')} "
                    f"(Stock: {product.stock})"
                )
                total_products += 1
            
            # Afficher les statistiques de la catégorie
            avg_price = category.products.aggregate(Avg('price'))['price__avg']
            self.stdout.write(
                f"  📊 {category.products.count()} produits - "
                f"Prix moyen: {avg_price:,.0f} FCFA\n"
            )
        
        # Résumé final
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✨ Terminé ! {Category.objects.count()} catégories, "
                f"{Product.objects.count()} produits créés"
            )
        )