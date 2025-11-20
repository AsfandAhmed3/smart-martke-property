from rest_framework import serializers
from .models import Property, Owner


class OwnerSerializer(serializers.ModelSerializer):
    properties_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Owner
        fields = [
            'id', 'name', 'email', 'phone', 'address', 'notes',
            'properties_count', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_properties_count(self, obj):
        return obj.properties.count()


class PropertyListSerializer(serializers.ModelSerializer):
    """Serializer for property list view"""
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    occupancy_rate = serializers.ReadOnlyField()
    roi = serializers.ReadOnlyField()
    
    class Meta:
        model = Property
        fields = [
            'id', 'name', 'property_type', 'status', 'address', 'city',
            'state', 'total_units', 'occupied_units', 'occupancy_rate',
            'current_value', 'monthly_revenue', 'roi', 'owner_name',
            'image_url', 'created_at'
        ]


class PropertyDetailSerializer(serializers.ModelSerializer):
    """Serializer for property detail view"""
    owner_details = OwnerSerializer(source='owner', read_only=True)
    occupancy_rate = serializers.ReadOnlyField()
    roi = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    
    class Meta:
        model = Property
        fields = [
            'id', 'name', 'property_type', 'status', 'address', 'city',
            'state', 'zip_code', 'country', 'full_address', 'total_units',
            'occupied_units', 'occupancy_rate', 'size_sqft', 'year_built',
            'purchase_price', 'current_value', 'monthly_revenue',
            'monthly_expenses', 'roi', 'owner', 'owner_details',
            'description', 'features', 'image_url', 'acquisition_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class PropertyCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating properties"""
    
    class Meta:
        model = Property
        fields = [
            'name', 'property_type', 'status', 'address', 'city', 'state',
            'zip_code', 'country', 'total_units', 'occupied_units',
            'size_sqft', 'year_built', 'purchase_price', 'current_value',
            'monthly_revenue', 'monthly_expenses', 'owner', 'description',
            'features', 'image_url', 'acquisition_date'
        ]
    
    def validate_occupied_units(self, value):
        """Ensure occupied units don't exceed total units"""
        total_units = self.initial_data.get('total_units', 0)
        if value > total_units:
            raise serializers.ValidationError(
                "Occupied units cannot exceed total units"
            )
        return value
