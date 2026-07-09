from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .cache import bump_cache_version
from .image_utils import generate_webp_variant, optimize_original_image
from .models import Category, Product, ProductImage


@receiver([post_save, post_delete], sender=Product)
@receiver([post_save, post_delete], sender=Category)
@receiver([post_save, post_delete], sender=ProductImage)
def invalidate_products_cache(sender, **kwargs):
    """Any product/category/gallery-image write makes every cached read stale —
    price and stock changes in particular must show up immediately."""
    bump_cache_version()


@receiver(post_save, sender=Product)
def generate_product_webp(sender, instance, **kwargs):
    if instance.image:
        optimize_original_image(instance.image)
        generate_webp_variant(instance.image)


@receiver(post_save, sender=ProductImage)
def generate_product_image_webp(sender, instance, **kwargs):
    if instance.image:
        optimize_original_image(instance.image)
        generate_webp_variant(instance.image)
