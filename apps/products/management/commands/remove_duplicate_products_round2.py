"""Second round of duplicate cleanup — this time for products with different
(misspelled/reworded) names but a byte-identical main image, found via
list_duplicate_images. Deletes the confirmed duplicate half of each pair and,
for two of them, corrects the surviving product's price to its known
original value (recovered import data) at the same time.

Deliberately does NOT touch id=29 / id=85 ("Hachoir/mixeur..." vs
"Éplucheur...") — same image, but genuinely different products with
different prices; one of them has the wrong photo assigned and needs a
real replacement image, not a delete."""
from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.products.models import Product

# (name of the product being deleted, id to delete)
IDS_TO_DELETE = [
    ('Pistolet vibro masseur RF - 321', 317),
    ('Caisse pour range bijoux et meckup', 274),
    ('Bosse de douche en silicone', 129),
    ('Lime ongle rechargeable GM', 265),
    ('Aerographe portable rechargeable avec compresseur (kit complet)', 264),
    ("Distributeur d'eau chaude et froide", 261),
    ("Classeur d'oeufs pliable", 260),
    ('Machine a lave HISENSE semi - automatique 13.5 KG', 245),
    ('Refrigerateur congelateur MIDEA MDRT 237 / 173L', 218),
    ('Miroir flexible autocollant HA-39', 134),
]

# (id of the surviving product, corrected price)
PRICE_FIXES = [
    (179, Decimal('18500')),  # Lime ongles rechargeable d'origine GM
    (180, Decimal('12000')),  # Aerographe portable pour ongles rechargeable numérique...
]


class Command(BaseCommand):
    help = "Deuxieme passe de nettoyage des doublons (nom different, image identique)."

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        deleted = 0
        fixed = 0

        for name, pid in IDS_TO_DELETE:
            try:
                product = Product.objects.get(id=pid, name=name)
            except Product.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"[introuvable, ignore] id={pid} name={name!r}"
                ))
                continue
            self.stdout.write(f"SUPPRIME  id={product.id}  {product.name!r}  prix={product.price}")
            if not dry_run:
                product.delete()
            deleted += 1

        for pid, new_price in PRICE_FIXES:
            try:
                product = Product.objects.get(id=pid)
            except Product.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"[introuvable, ignore] id={pid}"))
                continue
            self.stdout.write(f"PRIX      id={product.id}  {product.name!r}  {product.price} -> {new_price}")
            if not dry_run:
                product.price = new_price
                product.save(update_fields=['price'])
            fixed += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f"{'[DRY RUN] ' if dry_run else ''}{deleted} produit(s) supprime(s), {fixed} prix corrige(s)."
        ))
        self.stdout.write(self.style.WARNING(
            "Rappel : id=29 'Hachoir/mixeur...' et id=85 'Éplucheur...' partagent "
            "la meme image mais sont des produits differents - non touches ici, "
            "il faut uploader la bonne photo pour l'un des deux manuellement."
        ))
