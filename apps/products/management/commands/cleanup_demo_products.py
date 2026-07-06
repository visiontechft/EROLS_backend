from django.core.management.base import BaseCommand

from apps.products.models import Category, Product

DEMO_CATEGORY_SLUGS = [
    'electronique-smartphones',
    'mode-vetements',
    'maison-electromenager',
    'beaute-soins',
    'jouets-enfants',
]


class Command(BaseCommand):
    help = (
        "Supprime les produits et categories de demonstration crees par "
        "seed_products.py (photos Unsplash, donnees fictives) — a lancer une "
        "fois le vrai catalogue importe via import_whatsapp_catalog."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Affiche ce qui serait supprime sans ecrire en base",
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        categories = Category.objects.filter(slug__in=DEMO_CATEGORY_SLUGS)

        if not categories.exists():
            self.stdout.write(self.style.WARNING("Aucune categorie de demonstration trouvee."))
            return

        for category in categories:
            products = Product.objects.filter(category=category)
            count = products.count()
            if dry_run:
                self.stdout.write(f"[dry-run] Categorie '{category.name}' : {count} produit(s) a supprimer")
                for p in products:
                    self.stdout.write(f"[dry-run]   - {p.name}")
                continue
            products.delete()
            category.delete()
            self.stdout.write(self.style.SUCCESS(
                f"Categorie '{category.name}' supprimee ({count} produit(s))"
            ))

        if dry_run:
            self.stdout.write(self.style.WARNING("\n[dry-run] Aucune ecriture en base."))
