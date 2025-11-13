from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id', 'name', 'description',
            'can_create_properties', 'can_edit_properties', 'can_delete_properties',
            'can_manage_tenants', 'can_manage_leases', 'can_manage_financials',
            'can_manage_users', 'can_view_analytics', 'can_export_reports'
        ]


class UserSerializer(serializers.ModelSerializer):
    role_details = RoleSerializer(source='role', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'full_name', 'phone', 'date_of_birth', 'avatar', 'role', 'role_details',
            'mfa_enabled', 'email_notifications', 'lease_reminders',
            'maintenance_alerts', 'payment_notifications',
            'is_active', 'date_joined', 'last_login', 'created_at'
        ]
        read_only_fields = ['created_at', 'date_joined', 'last_login']


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'date_of_birth', 'avatar'
        ]


class NotificationPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email_notifications', 'lease_reminders',
            'maintenance_alerts', 'payment_notifications'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name',
            'password', 'password_confirm'
        ]
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            
            data['user'] = user
            return data
        
        raise serializers.ValidationError('Must include "email" and "password".')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("New passwords do not match")
        return data
