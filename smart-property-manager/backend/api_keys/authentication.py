from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from .models import APIKey, APIKeyUsageLog
import time


class APIKeyAuthentication(BaseAuthentication):
    """
    Custom authentication class for API Key authentication
    
    Usage:
    Include API key in request header:
    Authorization: ApiKey <your-api-key>
    """
    
    keyword = 'ApiKey'
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith(f'{self.keyword} '):
            return None  # Not an API key authentication attempt
        
        # Extract API key from header
        try:
            api_key = auth_header.split(' ')[1]
        except IndexError:
            raise AuthenticationFailed('Invalid API key header format')
        
        # Extract key prefix (first 8 characters)
        if len(api_key) < 8:
            raise AuthenticationFailed('Invalid API key format')
        
        key_prefix = api_key[:8]
        
        # Find API key by prefix
        try:
            api_key_obj = APIKey.objects.select_related('user').get(key_prefix=key_prefix)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')
        
        # Verify the full key
        if not api_key_obj.verify_key(api_key):
            raise AuthenticationFailed('Invalid API key')
        
        # Check if key is active
        if not api_key_obj.is_active:
            raise AuthenticationFailed('API key is inactive')
        
        # Check if key is expired
        if api_key_obj.is_expired():
            raise AuthenticationFailed('API key has expired')
        
        # Check IP address if restricted
        ip_address = self.get_client_ip(request)
        if not api_key_obj.check_ip_allowed(ip_address):
            raise AuthenticationFailed(f'Access denied from IP address: {ip_address}')
        
        # Store API key object in request for rate limiting middleware
        request.api_key = api_key_obj
        request.start_time = time.time()
        
        # Return user and api_key_obj as auth tuple
        return (api_key_obj.user, api_key_obj)
    
    def authenticate_header(self, request):
        """
        Return authentication header for 401 responses
        """
        return self.keyword
    
    def get_client_ip(self, request):
        """
        Get client IP address from request
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
