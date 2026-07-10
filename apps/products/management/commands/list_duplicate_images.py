"""Groups products by the MD5 checksum of their main image, regardless of
name — catches the case list_duplicate_names misses: the same photo reused
across products that were given different names during data entry (typos,
rewording, "numerique" vs "d'origine", etc.), which looks like near-duplicate
clutter on the storefront even though no two names match exactly.

Only flags products that actually have an image file; products without one
are skipped since there's nothing to hash.
"""
import hashlib
from collections import defaultdict

from django.core.management.base import BaseCommand

from apps.products.models import Product


class Command(BaseCommand):
    help = "Regroupe les produits dont l'image principale est strictement identique (checksum), peu importe le nom."

    def handle(self, *args, **options):
        by_hash = defaultdict(list)
        skipped = 0

        for product in Product.objects.exclude(image='').exclude(image__isnull=True):
            try:
                product.image.open('rb')
                digest = hashlib.md5(product.image.read()).hexdigest()
            except Exception:
                skipped += 1
                continue
            finally:
                try:
                    product.image.close()
                except Exception:
                    pass
            by_hash[digest].append(product)

        groups = {h: plist for h, plist in by_hash.items() if len(plist) > 1}

        if not groups:
            self.stdout.write(self.style.SUCCESS("Aucune image en double trouvee."))
        else:
            for digest, plist in groups.items():
                self.stdout.write('')
                self.stdout.write(self.style.WARNING(
                    f"Meme image ({digest[:8]}...) sur {len(plist)} produits :"
                ))
                for p in sorted(plist, key=lambda x: x.id):
                    self.stdout.write(
                        f"  id={p.id}  {p.name!r}  prix={p.price}  stock={p.stock}  image={p.image.url}"
                    )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f"{len(groups)} groupe(s) d'images en double "
            f"({sum(len(v) for v in groups.values())} produits concernes)."
        ))
        if skipped:
            self.stdout.write(self.style.WARNING(f"{skipped} produit(s) ignore(s) (image illisible)."))
