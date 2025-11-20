from rest_framework import serializers
from .models import Tenant
from properties.serializers import PropertyListSerializer


class TenantSerializer(serializers.ModelSerializer):
    property_details = PropertyListSerializer(source='property', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    initials = serializers.CharField(source='get_initials', read_only=True)
    
    class Meta:
        model = Tenant
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'initials',
            'email', 'phone', 'date_of_birth', 'ssn_last4',
            'employer', 'job_title', 'monthly_income', 'employment_length',
            'property', 'property_details', 'unit_number', 'status',
            'emergency_contact_name', 'emergency_contact_phone', 
            'emergency_contact_relationship',
            'move_in_date', 'move_out_date', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class TenantListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing tenants"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    initials = serializers.CharField(source='get_initials', read_only=True)
    property_name = serializers.CharField(source='property.name', read_only=True)
    
    class Meta:
        model = Tenant
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'initials',
            'email', 'phone', 'property', 'property_name', 'unit_number',
            'status', 'move_in_date', 'created_at'
        ]


class CreateTenantSerializer(serializers.ModelSerializer):
    """Serializer for creating tenants"""
    
    class Meta:
        model = Tenant
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'ssn_last4', 'employer', 'job_title',
            'monthly_income', 'employment_length', 'property',
            'unit_number', 'status', 'emergency_contact_name',
            'emergency_contact_phone', 'emergency_contact_relationship',
            'move_in_date', 'notes'
        ]
    
    def validate_email(self, value):
        if Tenant.objects.filter(email=value).exists():
            raise serializers.ValidationError("A tenant with this email already exists.")
        return value
