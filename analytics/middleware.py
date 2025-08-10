from django.utils.deprecation import MiddlewareMixin

class TrafficLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip logging for admin or static paths
        if request.path.startswith('/admin') or request.path.startswith('/static'):
            return None
        
        # For now, we'll just pass through without logging to database
        # Since we're using a dummy database and generating traffic data on-the-fly
        # This middleware can be enhanced later if needed
        return None
