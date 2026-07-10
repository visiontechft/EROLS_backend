"""Deletes confirmed duplicate products — same name, byte-identical product
photo (verified via MD5 checksum comparison outside this command) — keeping
the lowest id (the first uploaded) in each group and removing the rest.

The id list below is specific to this one cleanup, decided after visually/
checksum-verifying each group; it is not a generic "find duplicates" tool
(see list_duplicate_names for that)."""
from django.core.management.base import BaseCommand

from apps.products.models import Product

# (name, [ids to delete]) — the id NOT listed here is the one being kept.
GROUPS_TO_DELETE = [
    ('Aerographe portable rechargeable avec compresseur', [263]),
    ('Bafle rechargeable avec 1 micro a fil', [201]),
    ("Bafle rechargeable d'origine avec 1 micro balladeur", [249, 250]),
    ('Diffuseur de parfum', [161, 259, 273]),
    ('Lime à ongles rechargeable numérique', [184]),
    ('Matelas gonflable deux places', [303]),
    ('Mini climatiseur et diffuseur de parfum', [277]),
    ('Trotinette', [137]),
]


class Command(BaseCommand):
    help = "Supprime les produits en double confirmes (voir GROUPS_TO_DELETE)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="N'affiche que ce qui serait supprime, sans rien supprimer.",
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        deleted = 0

        for name, ids in GROUPS_TO_DELETE:
            for pid in ids:
                try:
                    product = Product.objects.get(id=pid, name=name)
                except Product.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f"[introuvable, ignore] id={pid} name={name!r} — "
                        f"deja supprime ou ne correspond plus a ce nom"
                    ))
                    continue

                self.stdout.write(f"id={product.id}  {product.name!r}  prix={product.price}")
                if not dry_run:
                    product.delete()
                deleted += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f"{'[DRY RUN] ' if dry_run else ''}{deleted} produit(s) {'a supprimer' if dry_run else 'supprime(s)'}."
        ))
