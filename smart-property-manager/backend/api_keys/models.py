import secrets
import hashlib
from django.db import models
from django.utils import timezone
from users.models import User


class APIKey(models.Model):
    """API Key model for external API access"""
    
    # User who owns the key
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    
    # Key identification
    name = models.CharField(max_length=255, help_text='Friendly name for the API key')
    key_prefix = models.CharField(max_length=8, unique=True, help_text='First 8 characters of the key')
    key_hash = models.CharField(max_length=64, help_text='SHA256 hash of the full key')
    
    # Permissions
    is_active = models.BooleanField(default=True)
    allowed_ips = models.TextField(blank=True, help_text='Comma-separated list of allowed IP addresses')
    rate_limit = models.IntegerField(default=1000, help_text='Requests per hour')
    
    # Scopes/Permissions
    can_read = models.BooleanField(default=True)
    can_write = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text='Optional expiration date')
    
    # Usage tracking
    usage_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['key_prefix']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.key_prefix}...)"
    
    @staticmethod
    def generate_key():
        """Generate a secure random API key"""
        return secrets.token_urlsafe(32)  # 256-bit key
    
    @staticmethod
    def hash_key(key):
        """Hash the API key using SHA256"""
        return hashlib.sha256(key.encode()).hexdigest()
    
    def verify_key(self, key):
        """Verify if the provided key matches the stored hash"""
        return self.key_hash == self.hash_key(key)
    
    def get_masked_key(self):
        """Return masked key for display (only shows prefix)"""
        return f"{self.key_prefix}{'*' * 40}"
    
    def is_expired(self):
        """Check if the API key is expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    def is_valid(self):
        """Check if the API key is valid (active and not expired)"""
        return self.is_active and not self.is_expired()
    
    def increment_usage(self):
        """Increment usage count and update last_used_at"""
        self.usage_count += 1
        self.last_used_at = timezone.now()
        self.save(update_fields=['usage_count', 'last_used_at'])
    
    def check_ip_allowed(self, ip_address):
        """Check if the IP address is allowed"""
        if not self.allowed_ips:
            return True  # No IP restriction
        allowed_list = [ip.strip() for ip in self.allowed_ips.split(',')]
        return ip_address in allowed_list
    
    def deactivate(self):
        """Deactivate the API key"""
        self.is_active = False
        self.save()
    
    def rotate(self):
        """Rotate the API key (generate new key, keep same settings)"""
        new_key = self.generate_key()
        self.key_prefix = new_key[:8]
        self.key_hash = self.hash_key(new_key)
        self.created_at = timezone.now()
        self.usage_count = 0
        self.last_used_at = None
        self.save()
        return new_key


class APIKeyUsageLog(models.Model):
    """Log API key usage for auditing"""
    
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE, related_name='usage_logs')
    
    # Request details
    endpoint = models.CharField(max_length=500)
    method = models.CharField(max_length=10)  # GET, POST, PUT, DELETE
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    
    # Response
    status_code = models.IntegerField()
    response_time = models.FloatField(help_text='Response time in seconds')
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['api_key', 'timestamp']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['status_code']),
        ]
    
    def __str__(self):
        return f"{self.api_key.name} - {self.method} {self.endpoint} ({self.status_code})"
