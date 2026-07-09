"""Local image optimization: generate a resized WebP sibling for every product
photo at upload time (no external CDN/service — see the explicit decision to
stay local-only). Served directly by nginx/whitenoise like the originals.
"""
import os
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image

MAX_DIMENSION = 1600  # product photos rarely need to be larger client-side
WEBP_QUALITY = 82


def webp_path_for(image_field) -> str | None:
    """Returns the storage path the WebP sibling would have, without checking
    whether it exists yet."""
    if not image_field or not image_field.name:
        return None
    root, _ext = os.path.splitext(image_field.name)
    return f'{root}.webp'


def generate_webp_variant(image_field) -> None:
    """Creates a resized WebP sibling next to the original image (same path,
    .webp extension) if one doesn't already exist. Safe to call repeatedly —
    it's a no-op once the file has been generated."""
    webp_name = webp_path_for(image_field)
    if not webp_name:
        return

    storage = image_field.storage
    if storage.exists(webp_name):
        return

    try:
        image_field.open('rb')
        img = Image.open(image_field)
        img.load()
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGBA' if img.mode == 'P' and 'transparency' in img.info else 'RGB')
        img.thumbnail((MAX_DIMENSION, MAX_DIMENSION))

        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=WEBP_QUALITY)
        buffer.seek(0)
        storage.save(webp_name, ContentFile(buffer.read()))
    except Exception:
        # A bad/corrupt upload shouldn't break the save() call that triggered
        # this — the product just keeps serving its original image format.
        pass
    finally:
        try:
            image_field.close()
        except Exception:
            pass
