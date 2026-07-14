"""Applique le barème de revente confirmé (erols_frontend/src/lib/priceTiers.ts)
aux 22 produits importés par import_visiontech_batch3, qui avaient été crees
avec leur prix d'achat brut au lieu du prix de vente.

Ne touche qu'aux slugs listes ici — pas d'appel a l'action globale
bulk-price-tiers, qui aurait re-applique le bonus a tous les autres produits
deja corriges precedemment (double ajustement).

Idempotent : ne modifie un produit que si son prix actuel correspond encore
au prix d'achat brut attendu (evite un double ajustement si relance)."""
from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.products.models import Product

# Barème confirmé (identique à PRICE_TIERS côté frontend) : bonus fixe par
# palier de prix d'achat.
PRICE_TIERS = [
    (0, 499, 300),
    (500, 1499, 500),
    (1500, 3999, 1000),
    (4000, 19999, 2000),
    (20000, 49999, 3000),
    (50000, None, 5000),
]


def apply_tier_bonus(cost_price):
    for min_price, max_price, bonus in PRICE_TIERS:
        if cost_price >= min_price and (max_price is None or cost_price <= max_price):
            return cost_price + bonus
    return cost_price


# (slug, prix d'achat brut attendu tel qu'importe)
RAW_PRICES = [
    ('ampoule-led-tntorch-four-circle-ufo-light-60w', 2500),
    ('papier-peint-autocollant-marbre-3m-x-1-20m', 7000),
    ('mp3-auto-bluetooth-x33', 1500),
    ('ring-light-22-rgb-complet-avec-trepied', 20000),
    ('ring-light-14-complet-rgb', 7000),
    ('ring-light-12-rgb-avec-trepied', 5000),
    ('ruban-adhesif-de-masquage-rouleau', 400),
    ('power-bank-xnen-xn-743-50000mah', 10000),
    ('support-telephone-gimbal-stabilisateur-q31', 9000),
    ('support-telephone-gimbal-q515-tk', 12000),
    ('casque-bluetooth-pliable-p39', 2000),
    ('rallonge-multiprise-ingelec-5-trous', 2000),
    ('tensiometre-electronique-arm-style', 3000),
    ('torche-rechargeable-zoom-telescopique-636-3', 1500),
    ('cordon-usb-8600-long', 300),
    ('cordon-usb-type-c-long', 400),
    ('souris-usb-optique-filaire', 500),
    ('piles-duracell-plus-aa-x4', 500),
    ('jeu-de-tournevis-de-precision-toolux', 3500),
    ('batterie-solaire-cclamp-12v-7ah', 4000),
    ('torche-rechargeable-cob-avec-crochet', 1000),
    ('support-telephone-selfie-stick-k28', 6500),
]


class Command(BaseCommand):
    help = "Applique le barème de revente aux 22 produits du batch3 visiontech (prix d'achat -> prix de vente)."

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        updated = 0
        skipped = 0

        for slug, raw_price in RAW_PRICES:
            try:
                product = Product.objects.get(slug=slug)
            except Product.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"[introuvable, ignore] {slug}"))
                continue

            raw_price = Decimal(raw_price)
            if product.price != raw_price:
                self.stdout.write(self.style.WARNING(
                    f"[deja ajuste, ignore] {product.name!r}: prix actuel {product.price} "
                    f"!= prix d'achat brut attendu {raw_price}"
                ))
                skipped += 1
                continue

            new_price = apply_tier_bonus(raw_price)
            self.stdout.write(f"{product.name!r}: {product.price} -> {new_price}")
            if not dry_run:
                product.price = new_price
                product.save(update_fields=['price'])
            updated += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f"{'[DRY RUN] ' if dry_run else ''}{updated} produit(s) {'a corriger' if dry_run else 'corrige(s)'}, "
            f"{skipped} deja a jour/ignore(s)."
        ))
