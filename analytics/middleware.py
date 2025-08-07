from .models import TrafficLog
from django.utils.deprecation import MiddlewareMixin

class TrafficLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin') or request.path.startswith('/static'):
            return  # Skip logging for admin or static paths

        ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        referrer = request.META.get('HTTP_REFERER', '')

        TrafficLog.objects.create(
            path=request.path,
            method=request.method,
            ip_address=ip,
            user_agent=user_agent,
            referrer=referrer,
            website=None  # Set to None since we don't have website info in middleware
        )
