import time
from functools import wraps
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status

# Settings for rate limiting
RATE_LIMIT = 5  # max requests
TIME_WINDOW = 60  # seconds


def rate_limit(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        # Identify client by user id if authenticated, else by IP
        if request.user.is_authenticated:
            ident = f'user-{request.user.id}'
        else:
            ident = f'ip-{request.META.get("REMOTE_ADDR")}'
        cache_key = f'rate-limit:{ident}:{request.path}'
        data = cache.get(cache_key, {'count': 0, 'start': time.time()})
        now = time.time()
        if now - data['start'] > TIME_WINDOW:
            data = {'count': 1, 'start': now}
        else:
            data['count'] += 1
        cache.set(cache_key, data, timeout=TIME_WINDOW)
        if data['count'] > RATE_LIMIT:
            return Response({'detail': 'Too many requests. Please try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        return view_func(self, request, *args, **kwargs)
    return _wrapped_view 