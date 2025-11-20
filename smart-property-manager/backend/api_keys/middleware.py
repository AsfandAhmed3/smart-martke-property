from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.core.cache import cache
from django.utils import timezone
import time
from .models import APIKeyUsageLog


class APIKeyMiddleware(MiddlewareMixin):
    """
    Middleware for API key rate limiting and usage logging
    """
    
    def process_request(self, request):
        """
        Process request for API key rate limiting
        """
        # Check if request has API key authentication
        if hasattr(request, 'api_key'):
            api_key = request.api_key
            
            # Check rate limit
            cache_key = f'api_key_rate_limit_{api_key.id}'
            current_count = cache.get(cache_key, 0)
            
            if current_count >= api_key.rate_limit:
                return JsonResponse({
                    'error': 'Rate limit exceeded',
                    'limit': api_key.rate_limit,
                    'period': '1 hour',
                    'message': f'You have exceeded the rate limit of {api_key.rate_limit} requests per hour'
                }, status=429)
            
            # Increment rate limit counter
            cache.set(cache_key, current_count + 1, 3600)  # 1 hour TTL
            
            # Check write/delete permissions for non-GET requests
            if request.method not in ['GET', 'HEAD', 'OPTIONS']:
                if request.method == 'DELETE' and not api_key.can_delete:
                    return JsonResponse({
                        'error': 'Permission denied',
                        'message': 'This API key does not have delete permission'
                    }, status=403)
                elif request.method in ['POST', 'PUT', 'PATCH'] and not api_key.can_write:
                    return JsonResponse({
                        'error': 'Permission denied',
                        'message': 'This API key does not have write permission'
                    }, status=403)
            elif not api_key.can_read:
                return JsonResponse({
                    'error': 'Permission denied',
                    'message': 'This API key does not have read permission'
                }, status=403)
        
        return None
    
    def process_response(self, request, response):
        """
        Log API key usage after response
        """
        # Log usage if API key was used
        if hasattr(request, 'api_key') and hasattr(request, 'start_time'):
            api_key = request.api_key
            
            # Calculate response time
            response_time = time.time() - request.start_time
            
            # Get client IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR', '')
            
            # Log usage asynchronously (in production, use Celery)
            try:
                APIKeyUsageLog.objects.create(
                    api_key=api_key,
                    endpoint=request.path,
                    method=request.method,
                    ip_address=ip_address,
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                    status_code=response.status_code,
                    response_time=response_time
                )
                
                # Increment usage count on API key
                api_key.increment_usage()
            except Exception as e:
                # Silently fail - don't break the request
                print(f"Failed to log API key usage: {e}")
        
        return response
