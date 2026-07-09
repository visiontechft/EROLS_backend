from django.core.management.base import BaseCommand

from apps.products.image_utils import generate_webp_variant
from apps.products.models import Product, ProductImage


class Command(BaseCommand):
    help = "Genere les variantes WebP manquantes pour les produits et photos de galerie deja en base."

    def handle(self, *args, **options):
        done = 0

        for product in Product.objects.exclude(image='').exclude(image__isnull=True):
            if product.image:
                generate_webp_variant(product.image)
                done += 1

        for image in ProductImage.objects.exclude(image='').exclude(image__isnull=True):
            generate_webp_variant(image.image)
            done += 1

        self.stdout.write(self.style.SUCCESS(f"Termine : {done} image(s) traitee(s)."))
