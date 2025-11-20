from rest_framework import serializers
from .models import APIKey, APIKeyUsageLog
from users.serializers import UserSerializer


class APIKeySerializer(serializers.ModelSerializer):
    """Serializer for APIKey with full details"""
    user_details = UserSerializer(source='user', read_only=True)
    masked_key = serializers.CharField(source='get_masked_key', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    days_until_expiry = serializers.SerializerMethodField()
    
    class Meta:
        model = APIKey
        fields = [
            'id', 'user', 'user_details', 'name', 'key_prefix', 'masked_key',
            'is_active', 'allowed_ips', 'rate_limit',
            'can_read', 'can_write', 'can_delete',
            'created_at', 'last_used_at', 'expires_at',
            'is_expired', 'is_valid', 'days_until_expiry',
            'usage_count'
        ]
        read_only_fields = ['user', 'key_prefix', 'created_at', 'last_used_at', 'usage_count']
    
    def get_days_until_expiry(self, obj):
        if obj.expires_at:
            from django.utils import timezone
            delta = obj.expires_at - timezone.now()
            return delta.days if delta.days > 0 else 0
        return None
    
    def get_is_expired(self, obj):
        return obj.is_expired()
    
    def get_is_valid(self, obj):
        return obj.is_valid()


class APIKeyListSerializer(serializers.ModelSerializer):
    """Simplified serializer for API key list"""
    masked_key = serializers.CharField(source='get_masked_key', read_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = APIKey
        fields = [
            'id', 'name', 'masked_key', 'is_active', 'is_valid',
            'created_at', 'last_used_at', 'usage_count'
        ]
    
    def get_is_valid(self, obj):
        return obj.is_valid()


class CreateAPIKeySerializer(serializers.ModelSerializer):
    """Serializer for creating API keys"""
    class Meta:
        model = APIKey
        fields = [
            'name', 'allowed_ips', 'rate_limit',
            'can_read', 'can_write', 'can_delete', 'expires_at'
        ]
    
    def validate_rate_limit(self, value):
        if value < 1:
            raise serializers.ValidationError("Rate limit must be at least 1")
        if value > 10000:
            raise serializers.ValidationError("Rate limit cannot exceed 10000 requests per hour")
        return value


class UpdateAPIKeySerializer(serializers.ModelSerializer):
    """Serializer for updating API key settings"""
    class Meta:
        model = APIKey
        fields = [
            'name', 'is_active', 'allowed_ips', 'rate_limit',
            'can_read', 'can_write', 'can_delete', 'expires_at'
        ]


class APIKeyResponseSerializer(serializers.Serializer):
    """Serializer for API key creation response (includes plain key)"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    key = serializers.CharField(help_text='Full API key - save this, it will not be shown again')
    key_prefix = serializers.CharField()
    masked_key = serializers.CharField()
    created_at = serializers.DateTimeField()
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    message = serializers.CharField()


class APIKeyUsageLogSerializer(serializers.ModelSerializer):
    """Serializer for APIKeyUsageLog"""
    api_key_name = serializers.CharField(source='api_key.name', read_only=True)
    
    class Meta:
        model = APIKeyUsageLog
        fields = [
            'id', 'api_key', 'api_key_name', 'endpoint', 'method',
            'ip_address', 'user_agent', 'status_code', 'response_time',
            'timestamp'
        ]


class APIKeyStatisticsSerializer(serializers.Serializer):
    """Serializer for API key statistics"""
    total_keys = serializers.IntegerField()
    active_keys = serializers.IntegerField()
    inactive_keys = serializers.IntegerField()
    expired_keys = serializers.IntegerField()
    total_usage = serializers.IntegerField()
    usage_by_key = serializers.DictField()
    recent_usage = serializers.ListField()
    usage_by_endpoint = serializers.DictField()
    usage_by_status = serializers.DictField()
