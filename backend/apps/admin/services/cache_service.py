from django.core.cache import cache

DEFAULT_TIMEOUT = 60  # seconds


def cached(key, fn, timeout=DEFAULT_TIMEOUT):
    data = cache.get(key)
    if data is not None:
        return data

    data = fn()
    cache.set(key, data, timeout)
    return data
