from django.utils.deprecation import MiddlewareMixin
from .models import TrafficLog

class TrafficLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip logging for admin or static paths
        if request.path.startswith('/admin') or request.path.startswith('/static'):
            return None
        
        try:
            # Log traffic data to PostgreSQL database
            TrafficLog.objects.create(
                path=request.path,
                method=request.method,
                ip_address=request.META.get('REMOTE_ADDR', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                referrer=request.META.get('HTTP_REFERER', ''),
                website=None  # Will be set when website is created
            )
        except Exception as e:
            # Log error but don't crash the request
            print(f"⚠️  Traffic logging error: {e}")
        
        return None
