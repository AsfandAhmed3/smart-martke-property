from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tenant
from .serializers import (
    TenantSerializer,
    TenantListSerializer,
    CreateTenantSerializer
)


class TenantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Tenant CRUD operations
    """
    permission_classes = [IsAuthenticated]
    queryset = Tenant.objects.select_related('property').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'property']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'unit_number']
    ordering_fields = ['created_at', 'first_name', 'last_name', 'move_in_date']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TenantListSerializer
        elif self.action == 'create':
            return CreateTenantSerializer
        return TenantSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by property if provided
        property_id = self.request.query_params.get('property_id', None)
        if property_id:
            queryset = queryset.filter(property_id=property_id)
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get tenant statistics"""
        total = Tenant.objects.count()
        active = Tenant.objects.filter(status='active').count()
        inactive = Tenant.objects.filter(status='inactive').count()
        pending = Tenant.objects.filter(status='pending').count()
        
        return Response({
            'total': total,
            'active': active,
            'inactive': inactive,
            'pending': pending
        })
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a tenant"""
        tenant = self.get_object()
        tenant.status = 'active'
        tenant.save()
        
        serializer = self.get_serializer(tenant)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a tenant"""
        tenant = self.get_object()
        tenant.status = 'inactive'
        tenant.save()
        
        serializer = self.get_serializer(tenant)
        return Response(serializer.data)

