"""Importe le catalogue recu via WhatsApp le 14/07/2026 (22 produits) : cree
les produits avec prix reels, et leur photo depuis
import_data/batch3_visiontech/.

La plupart des photos sont des versions optimisees via ChatGPT (fond
nettoye/recompose) fournies par le client ; 5 produits sans version
optimisee gardent leur photo WhatsApp d'origine. Deux produits (power bank
XNEN, casque P39) ont une deuxieme photo en galerie."""
import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from apps.products.models import Category, Product, ProductImage

IMAGE_DIR = os.path.join(settings.BASE_DIR, 'import_data', 'batch3_visiontech')

DEFAULT_STOCK = 20

CATEGORIES = {
    'electronique': 'Électronique',
    'materiaux-revetements': 'Matériaux & Revêtements',
    'maison-decoration': 'Maison & Décoration',
}

PRODUCTS = [
    {
        'name': 'Ampoule LED TNTORCH Four-Circle UFO Light 60W',
        'slug': 'ampoule-led-tntorch-four-circle-ufo-light-60w',
        'category': 'electronique',
        'description': "Ampoule LED UFO 4 panneaux TNTORCH, 60W, 6500K, jusqu'à 90% d'économie d'énergie, culot à visser standard.",
        'price': 3500,  # 2500 + 1000 (barème 1500-3999)
        'images': ['ampoule-led-tntorch-four-circle-ufo-light-60w-1.jpg'],
    },
    {
        'name': 'Papier peint autocollant marbre 3M×1.20M',
        'slug': 'papier-peint-autocollant-marbre-3m-x-1-20m',
        'category': 'materiaux-revetements',
        'description': "Rouleau de papier peint autocollant effet marbre doré, 3m x 1,20m, pose facile sans colle.",
        'price': 9000,  # 7000 + 2000 (barème 4000-19999)
        'images': ['papier-peint-autocollant-marbre-3m-x-1-20m-1.png'],
    },
    {
        'name': 'MP3 auto Bluetooth X33',
        'slug': 'mp3-auto-bluetooth-x33',
        'category': 'electronique',
        'description': "Transmetteur FM Bluetooth voiture avec lumière RGB, charge rapide PD, sortie 45W, écran de fréquence.",
        'price': 2500,  # 1500 + 1000 (barème 1500-3999)
        'images': ['mp3-auto-bluetooth-x33-1.png'],
    },
    {
        'name': 'Ring light 22" RGB complet avec trépied',
        'slug': 'ring-light-22-rgb-complet-avec-trepied',
        'category': 'electronique',
        'description': "Anneau lumineux LED RGB 56cm (22 pouces) avec trépied, télécommande et support téléphone.",
        'price': 23000,  # 20000 + 3000 (barème 20000-49999)
        'images': ['ring-light-22-rgb-complet-avec-trepied-1.png'],
    },
    {
        'name': 'Ring light 14" complet RGB',
        'slug': 'ring-light-14-complet-rgb',
        'category': 'electronique',
        'description': "Anneau lumineux LED RGB 14 pouces avec trépied réglable et support téléphone rotatif.",
        'price': 9000,  # 7000 + 2000 (barème 4000-19999)
        'images': ['ring-light-14-complet-rgb-1.jpg'],
    },
    {
        'name': 'Ring light 12" RGB avec trépied',
        'slug': 'ring-light-12-rgb-avec-trepied',
        'category': 'electronique',
        'description': "Anneau lumineux LED RGB 12 pouces (LJJ-30) avec trépied et support téléphone.",
        'price': 7000,  # 5000 + 2000 (barème 4000-19999)
        'images': ['ring-light-12-rgb-avec-trepied-1.png'],
    },
    {
        'name': 'Ruban adhésif de masquage (rouleau)',
        'slug': 'ruban-adhesif-de-masquage-rouleau',
        'category': 'materiaux-revetements',
        'description': "Ruban adhésif de masquage crêpe, haute adhérence. Vendu à l'unité (pack de 9 rouleaux disponible sur demande).",
        'price': 700,  # 400 + 300 (barème 0-499)
        'images': ['ruban-adhesif-de-masquage-rouleau-1.png'],
    },
    {
        'name': "Power bank XNEN XN-743 50000mAh",
        'slug': 'power-bank-xnen-xn-743-50000mah',
        'category': 'electronique',
        'description': "Batterie externe grande capacité 50000mAh, charge rapide, écran LED, plusieurs ports de sortie.",
        'price': 12000,  # 10000 + 2000 (barème 4000-19999)
        'images': [
            'power-bank-xnen-xn-743-50000mah-1.png',
            'power-bank-xnen-xn-743-50000mah-2.png',
        ],
    },
    {
        'name': 'Support téléphone gimbal stabilisateur Q31',
        'slug': 'support-telephone-gimbal-stabilisateur-q31',
        'category': 'electronique',
        'description': "Stabilisateur gimbal pour smartphone, moteur brushless, trépied intégré, compatible iOS/Android.",
        'price': 11000,  # 9000 + 2000 (barème 4000-19999)
        'images': ['support-telephone-gimbal-stabilisateur-q31-1.png'],
    },
    {
        'name': 'Support téléphone gimbal Q515 TK',
        'slug': 'support-telephone-gimbal-q515-tk',
        'category': 'electronique',
        'description': "Perche à selfie gimbal stabilisateur avec télécommande sans fil, hauteur 1,01m, port USB-C.",
        'price': 14000,  # 12000 + 2000 (barème 4000-19999)
        'images': ['support-telephone-gimbal-q515-tk-1.jpg'],
    },
    {
        'name': 'Casque Bluetooth pliable P39',
        'slug': 'casque-bluetooth-pliable-p39',
        'category': 'electronique',
        'description': "Casque Bluetooth sans fil pliable, disponible en plusieurs coloris pastel.",
        'price': 3000,  # 2000 + 1000 (barème 1500-3999)
        'images': [
            'casque-bluetooth-pliable-p39-1.png',
            'casque-bluetooth-pliable-p39-2.png',
        ],
    },
    {
        'name': 'Rallonge multiprise Ingelec 5 trous',
        'slug': 'rallonge-multiprise-ingelec-5-trous',
        'category': 'electronique',
        'description': "Multiprise parasurtenseur 3600W/250V, 5 sorties, interrupteur lumineux.",
        'price': 3000,  # 2000 + 1000 (barème 1500-3999)
        'images': ['rallonge-multiprise-ingelec-5-trous-1.png'],
    },
    {
        'name': 'Tensiomètre électronique Arm Style',
        'slug': 'tensiometre-electronique-arm-style',
        'category': 'electronique',
        'description': "Tensiomètre électronique de bras avec écran LCD, mesure automatique, brassard réglable 22-32cm.",
        'price': 4000,  # 3000 + 1000 (barème 1500-3999)
        'images': ['tensiometre-electronique-arm-style-1.png'],
    },
    {
        'name': 'Torche rechargeable zoom télescopique 636-3',
        'slug': 'torche-rechargeable-zoom-telescopique-636-3',
        'category': 'electronique',
        'description': "Lampe torche rechargeable zoom télescopique, mousqueton intégré, port USB-C.",
        'price': 2500,  # 1500 + 1000 (barème 1500-3999)
        'images': ['torche-rechargeable-zoom-telescopique-636-3-1.png'],
    },
    {
        'name': 'Cordon USB 8600 (long)',
        'slug': 'cordon-usb-8600-long',
        'category': 'electronique',
        'description': "Cordon de charge/données USB, longueur standard, plusieurs coloris.",
        'price': 600,  # 300 + 300 (barème 0-499)
        'images': ['cordon-usb-8600-long-1.jpg'],
    },
    {
        'name': 'Cordon USB Type-C (long)',
        'slug': 'cordon-usb-type-c-long',
        'category': 'electronique',
        'description': "Cordon de charge/données USB Type-C, longueur renforcée, plusieurs coloris.",
        'price': 700,  # 400 + 300 (barème 0-499)
        'images': ['cordon-usb-type-c-long-1.png'],
    },
    {
        'name': 'Souris USB optique filaire',
        'slug': 'souris-usb-optique-filaire',
        'category': 'electronique',
        'description': "Souris optique filaire USB, molette de défilement, compatible tous PC.",
        'price': 1000,  # 500 + 500 (barème 500-1499)
        'images': ['souris-usb-optique-filaire-1.png'],
    },
    {
        'name': 'Piles Duracell Plus AA (x4)',
        'slug': 'piles-duracell-plus-aa-x4',
        'category': 'electronique',
        'description': "Pack de 4 piles alcalines Duracell Plus AA, +100% de durée de vie.",
        'price': 1000,  # 500 + 500 (barème 500-1499)
        'images': ['piles-duracell-plus-aa-x4-1.png'],
    },
    {
        'name': 'Jeu de tournevis de précision Toolux',
        'slug': 'jeu-de-tournevis-de-precision-toolux',
        'category': 'maison-decoration',
        'description': "Coffret tournevis de précision avec embouts multiples et douilles, mallette de rangement.",
        'price': 4500,  # 3500 + 1000 (barème 1500-3999)
        'images': ['jeu-de-tournevis-de-precision-toolux-1.png'],
    },
    {
        'name': 'Batterie solaire CCLAMP 12V/7AH',
        'slug': 'batterie-solaire-cclamp-12v-7ah',
        'category': 'electronique',
        'description': "Batterie solaire rechargeable scellée 12V/7AH, pour kit solaire ou éclairage d'urgence.",
        'price': 6000,  # 4000 + 2000 (barème 4000-19999)
        'images': ['batterie-solaire-cclamp-12v-7ah-1.png'],
    },
    {
        'name': 'Torche rechargeable COB avec crochet',
        'slug': 'torche-rechargeable-cob-avec-crochet',
        'category': 'electronique',
        'description': "Lampe torche rechargeable avec bande LED COB latérale, mousqueton, port USB-C.",
        'price': 1500,  # 1000 + 500 (barème 500-1499)
        'images': ['torche-rechargeable-cob-avec-crochet-1.png'],
    },
    {
        'name': 'Support téléphone selfie stick K28',
        'slug': 'support-telephone-selfie-stick-k28',
        'category': 'electronique',
        'description': "Perche à selfie pliable avec trépied, compatible streaming double téléphone.",
        'price': 8500,  # 6500 + 2000 (barème 4000-19999)
        'images': ['support-telephone-selfie-stick-k28-1.jpg'],
    },
]


class Command(BaseCommand):
    help = "Importe le catalogue WhatsApp du 14/07/2026 (22 produits, photos optimisees)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Affiche ce qui serait fait sans ecrire en base",
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        categories = {}
        for slug, name in CATEGORIES.items():
            if dry_run:
                self.stdout.write(f"[dry-run] Categorie: {name} ({slug})")
                continue
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'is_active': True},
            )
            categories[slug] = category
            tag = 'creee' if created else 'existante'
            self.stdout.write(self.style.SUCCESS(f"Categorie {tag}: {category.name}"))

        created_count = 0
        updated_count = 0
        missing_images = []

        for entry in PRODUCTS:
            slug = entry['slug']

            if dry_run:
                self.stdout.write(
                    f"[dry-run] Produit: {entry['name']} — {entry['price']} FCFA "
                    f"— {len(entry['images'])} image(s)"
                )
                continue

            category = categories[entry['category']]
            product, created = Product.objects.update_or_create(
                slug=slug,
                defaults=dict(
                    name=entry['name'],
                    description=entry['description'],
                    category=category,
                    price=entry['price'],
                    stock=DEFAULT_STOCK,
                    is_available=True,
                ),
            )
            created_count += 1 if created else 0
            updated_count += 0 if created else 1

            # Rebuild the gallery from scratch to keep the command idempotent on re-run.
            product.images.all().delete()

            for order, filename in enumerate(entry['images']):
                image_path = os.path.join(IMAGE_DIR, filename)
                if not os.path.isfile(image_path):
                    missing_images.append((entry['name'], filename))
                    continue

                with open(image_path, 'rb') as fh:
                    django_file = File(fh, name=filename)
                    if order == 0:
                        product.image.save(filename, django_file, save=True)
                        fh.seek(0)
                        ProductImage.objects.create(
                            product=product, image=File(fh, name=filename), order=0,
                        )
                    else:
                        ProductImage.objects.create(
                            product=product, image=django_file, order=order,
                        )

            tag = 'cree' if created else 'mis a jour'
            self.stdout.write(f"Produit {tag}: {product.name} ({entry['price']} FCFA)")

        if dry_run:
            self.stdout.write(self.style.WARNING(
                f"\n[dry-run] {len(PRODUCTS)} produit(s) seraient traites — aucune ecriture en base."
            ))
            return

        self.stdout.write(self.style.SUCCESS(
            f"\nTermine : {created_count} produit(s) cree(s), {updated_count} mis a jour."
        ))
        if missing_images:
            self.stdout.write(self.style.WARNING(
                f"{len(missing_images)} image(s) introuvable(s) (produit cree sans cette photo) :"
            ))
            for name, filename in missing_images:
                self.stdout.write(f"  - {name}: {filename}")
