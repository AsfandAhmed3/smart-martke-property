from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property, Owner
from .serializers import (
    PropertyListSerializer,
    PropertyDetailSerializer,
    PropertyCreateUpdateSerializer,
    OwnerSerializer
)


class PropertyViewSet(viewsets.ModelViewSet):
    """ViewSet for property CRUD operations"""
    queryset = Property.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property_type', 'status', 'city', 'state']
    search_fields = ['name', 'address', 'city', 'owner__name']
    ordering_fields = ['name', 'current_value', 'monthly_revenue', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PropertyListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PropertyCreateUpdateSerializer
        return PropertyDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get portfolio statistics"""
        properties = self.get_queryset()
        
        total_properties = properties.count()
        total_value = sum(p.current_value for p in properties)
        total_revenue = sum(p.monthly_revenue for p in properties)
        total_units = sum(p.total_units for p in properties)
        occupied_units = sum(p.occupied_units for p in properties)
        
        occupancy_rate = 0
        if total_units > 0:
            occupancy_rate = round((occupied_units / total_units) * 100, 1)
        
        return Response({
            'total_properties': total_properties,
            'total_value': total_value,
            'monthly_revenue': total_revenue,
            'occupancy_rate': occupancy_rate,
            'total_units': total_units,
            'occupied_units': occupied_units,
        })


class OwnerViewSet(viewsets.ModelViewSet):
    """ViewSet for owner CRUD operations"""
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering = ['name']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
