from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum
from django.utils import timezone
from .models import APIKey, APIKeyUsageLog
from .serializers import (
    APIKeySerializer,
    APIKeyListSerializer,
    CreateAPIKeySerializer,
    UpdateAPIKeySerializer,
    APIKeyResponseSerializer,
    APIKeyUsageLogSerializer,
    APIKeyStatisticsSerializer
)


class APIKeyViewSet(viewsets.ModelViewSet):
    """ViewSet for API Key management"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'key_prefix']
    ordering_fields = ['created_at', 'last_used_at', 'usage_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Users can only see their own API keys
        return APIKey.objects.filter(user=self.request.user).select_related('user')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return APIKeyListSerializer
        elif self.action == 'create':
            return CreateAPIKeySerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateAPIKeySerializer
        return APIKeySerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new API key and return the full key (only shown once)"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Generate API key
        api_key = APIKey.generate_key()
        
        # Create APIKey object
        api_key_obj = APIKey.objects.create(
            user=request.user,
            name=serializer.validated_data['name'],
            key_prefix=api_key[:8],
            key_hash=APIKey.hash_key(api_key),
            allowed_ips=serializer.validated_data.get('allowed_ips', ''),
            rate_limit=serializer.validated_data.get('rate_limit', 1000),
            can_read=serializer.validated_data.get('can_read', True),
            can_write=serializer.validated_data.get('can_write', False),
            can_delete=serializer.validated_data.get('can_delete', False),
            expires_at=serializer.validated_data.get('expires_at')
        )
        
        # Return response with full key
        response_data = {
            'id': api_key_obj.id,
            'name': api_key_obj.name,
            'key': api_key,  # Full key - only shown once!
            'key_prefix': api_key_obj.key_prefix,
            'masked_key': api_key_obj.get_masked_key(),
            'created_at': api_key_obj.created_at,
            'expires_at': api_key_obj.expires_at,
            'message': 'API key created successfully. Save this key - it will not be shown again!'
        }
        
        response_serializer = APIKeyResponseSerializer(response_data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def rotate(self, request, pk=None):
        """Rotate an API key (generate new key, keep settings)"""
        api_key_obj = self.get_object()
        
        # Generate new key
        new_key = api_key_obj.rotate()
        
        response_data = {
            'id': api_key_obj.id,
            'name': api_key_obj.name,
            'key': new_key,  # New full key - only shown once!
            'key_prefix': api_key_obj.key_prefix,
            'masked_key': api_key_obj.get_masked_key(),
            'created_at': api_key_obj.created_at,
            'expires_at': api_key_obj.expires_at,
            'message': 'API key rotated successfully. Save this new key - it will not be shown again!'
        }
        
        response_serializer = APIKeyResponseSerializer(response_data)
        return Response(response_serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate an API key"""
        api_key_obj = self.get_object()
        api_key_obj.deactivate()
        
        serializer = self.get_serializer(api_key_obj)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate an API key"""
        api_key_obj = self.get_object()
        api_key_obj.is_active = True
        api_key_obj.save()
        
        serializer = self.get_serializer(api_key_obj)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def usage_logs(self, request, pk=None):
        """Get usage logs for an API key"""
        api_key_obj = self.get_object()
        logs = api_key_obj.usage_logs.all()[:100]  # Last 100 logs
        
        serializer = APIKeyUsageLogSerializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get API key statistics"""
        queryset = self.get_queryset()
        
        total_keys = queryset.count()
        active_keys = queryset.filter(is_active=True).count()
        inactive_keys = queryset.filter(is_active=False).count()
        
        # Count expired keys
        now = timezone.now()
        expired_keys = queryset.filter(expires_at__lt=now).count()
        
        # Total usage
        total_usage = queryset.aggregate(total=Sum('usage_count'))['total'] or 0
        
        # Usage by key
        usage_by_key = {}
        for key in queryset:
            usage_by_key[key.name] = key.usage_count
        
        # Recent usage logs
        recent_logs = APIKeyUsageLog.objects.filter(
            api_key__user=request.user
        ).order_by('-timestamp')[:20]
        recent_usage = APIKeyUsageLogSerializer(recent_logs, many=True).data
        
        # Usage by endpoint
        usage_by_endpoint = {}
        endpoint_stats = APIKeyUsageLog.objects.filter(
            api_key__user=request.user
        ).values('endpoint').annotate(count=Count('id'))
        for stat in endpoint_stats:
            usage_by_endpoint[stat['endpoint']] = stat['count']
        
        # Usage by status code
        usage_by_status = {}
        status_stats = APIKeyUsageLog.objects.filter(
            api_key__user=request.user
        ).values('status_code').annotate(count=Count('id'))
        for stat in status_stats:
            usage_by_status[str(stat['status_code'])] = stat['count']
        
        data = {
            'total_keys': total_keys,
            'active_keys': active_keys,
            'inactive_keys': inactive_keys,
            'expired_keys': expired_keys,
            'total_usage': total_usage,
            'usage_by_key': usage_by_key,
            'recent_usage': recent_usage,
            'usage_by_endpoint': usage_by_endpoint,
            'usage_by_status': usage_by_status
        }
        
        serializer = APIKeyStatisticsSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def verify(self, request):
        """Verify if an API key is valid"""
        key = request.query_params.get('key')
        if not key:
            return Response(
                {'error': 'key parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract prefix
        key_prefix = key[:8]
        
        try:
            api_key_obj = APIKey.objects.get(key_prefix=key_prefix, user=request.user)
            
            if api_key_obj.verify_key(key):
                return Response({
                    'valid': api_key_obj.is_valid(),
                    'is_active': api_key_obj.is_active,
                    'is_expired': api_key_obj.is_expired(),
                    'name': api_key_obj.name,
                    'permissions': {
                        'can_read': api_key_obj.can_read,
                        'can_write': api_key_obj.can_write,
                        'can_delete': api_key_obj.can_delete
                    }
                })
            else:
                return Response(
                    {'valid': False, 'error': 'Invalid API key'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except APIKey.DoesNotExist:
            return Response(
                {'valid': False, 'error': 'API key not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class APIKeyUsageLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing API key usage logs"""
    permission_classes = [IsAuthenticated]
    serializer_class = APIKeyUsageLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['api_key', 'method', 'status_code']
    search_fields = ['endpoint', 'ip_address']
    ordering_fields = ['timestamp', 'response_time', 'status_code']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        # Users can only see logs for their own API keys
        return APIKeyUsageLog.objects.filter(
            api_key__user=self.request.user
        ).select_related('api_key')
