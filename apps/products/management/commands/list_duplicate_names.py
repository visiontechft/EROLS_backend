"""Lists products that share the exact same name but have different prices,
so a human can decide whether each group is a genuine accidental duplicate
(same item imported twice — safe to delete one) or several different
products that were given an identical, too-generic name at import time
(needs renaming + individually-correct prices, not deletion).

Prints each group with id, price, stock and image URL so they can be
compared visually without needing DB/admin access.
"""
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db.models import Count

from apps.products.models import Product


class Command(BaseCommand):
    help = "Liste les produits ayant exactement le meme nom, avec assez de details pour trancher."

    def handle(self, *args, **options):
        duplicate_names = (
            Product.objects.values('name')
            .annotate(n=Count('id'))
            .filter(n__gt=1)
            .order_by('name')
        )

        if not duplicate_names:
            self.stdout.write(self.style.SUCCESS("Aucun nom en double trouve."))
            return

        for row in duplicate_names:
            name = row['name']
            products = Product.objects.filter(name=name).order_by('id')
            self.stdout.write('')
            self.stdout.write(self.style.WARNING(f'"{name}" — {row["n"]} produits :'))
            for p in products:
                image = p.image.url if p.image else '(pas d\'image)'
                self.stdout.write(
                    f"  id={p.id}  slug={p.slug}  prix={p.price}  stock={p.stock}  image={image}"
                )
