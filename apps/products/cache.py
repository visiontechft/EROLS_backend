"""Cache versioning helper.

Instead of tracking every individual cache key touched by a write, each read
endpoint includes a "version" number in its cache key. A Product/Category/
ProductImage change just bumps the version once — every old key becomes
unreachable (and expires naturally later) without needing to enumerate or
delete anything. Simple, race-safe (INCR is atomic in Redis), no key drift.
"""
from django.core.cache import cache

VERSION_KEY = 'products:cache_version'

# Read-heavy, stable-shape endpoints only — the filterable /products/ list has
# too many query-param combinations to cache usefully and isn't included here.
TTL_SHORT = 60 * 5      # 5 min: homepage aggregate, featured/popular
TTL_MEDIUM = 60 * 15    # 15 min: categories, brands (change rarely)
TTL_DETAIL = 60 * 10    # 10 min: single product detail


def get_cache_version() -> int:
    version = cache.get(VERSION_KEY)
    if version is None:
        version = 1
        cache.set(VERSION_KEY, version, timeout=None)
    return version


def bump_cache_version() -> None:
    try:
        cache.incr(VERSION_KEY)
    except ValueError:
        # Key didn't exist yet (e.g. cache was flushed) — seed it.
        cache.set(VERSION_KEY, 2, timeout=None)


def versioned_key(*parts: str) -> str:
    return 'products:v{}:{}'.format(get_cache_version(), ':'.join(parts))
