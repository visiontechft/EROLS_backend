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
JPEG_QUALITY = 85
# Skip re-encoding files already under this size — avoids repeated quality loss
# on images that don't need it (and makes this a no-op on second save calls).
OPTIMIZE_SIZE_THRESHOLD = 400 * 1024


def optimize_original_image(image_field) -> None:
    """Resizes/re-compresses the uploaded file itself in place (same path, same
    format) so a 2-4MB phone photo doesn't sit on disk at full size forever —
    the WebP sibling below is what browsers actually load, but the original is
    still served as a fallback and still takes the space/upload time.
    Skipped when the file is already small and correctly sized."""
    if not image_field or not image_field.name:
        return

    storage = image_field.storage
    name = image_field.name

    try:
        image_field.open('rb')
        img = Image.open(image_field)
        img.load()
        original_size = image_field.size
        image_field.close()  # release the handle now — storage.delete() below
        # would otherwise fail with a PermissionError while it's still open.

        already_small_file = original_size <= OPTIMIZE_SIZE_THRESHOLD
        already_small_dimensions = img.width <= MAX_DIMENSION and img.height <= MAX_DIMENSION
        if already_small_file and already_small_dimensions:
            return  # nothing to gain by re-encoding

        original_format = (img.format or 'JPEG').upper()
        if original_format not in ('JPEG', 'JPG', 'PNG', 'WEBP'):
            return  # unusual format (GIF, etc.) — leave untouched

        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGBA' if 'transparency' in img.info else 'RGB')
        if original_format in ('JPEG', 'JPG') and img.mode == 'RGBA':
            img = img.convert('RGB')
        img.thumbnail((MAX_DIMENSION, MAX_DIMENSION))

        buffer = BytesIO()
        save_kwargs = (
            {'quality': JPEG_QUALITY, 'optimize': True}
            if original_format in ('JPEG', 'JPG')
            else {'optimize': True}
        )
        img.save(buffer, format=original_format, **save_kwargs)
        buffer.seek(0)
        optimized = buffer.read()

        # Only replace the stored file if we actually saved space.
        if len(optimized) < original_size:
            storage.delete(name)
            storage.save(name, ContentFile(optimized))
    except Exception:
        # A bad/corrupt upload shouldn't break the save() call that triggered
        # this — the product just keeps serving its original file untouched.
        pass
    finally:
        try:
            image_field.close()
        except Exception:
            pass


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
