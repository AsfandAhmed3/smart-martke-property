from rest_framework import serializers
from .models import Notification, NotificationPreference, NotificationTemplate
from users.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification with full details"""
    user_details = UserSerializer(source='user', read_only=True)
    type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_details', 'title', 'message',
            'notification_type', 'type_display', 'priority', 'priority_display',
            'is_read', 'read_at', 'related_object_type', 'related_object_id',
            'action_url', 'created_at', 'expires_at', 'is_expired'
        ]
        read_only_fields = ['user', 'created_at', 'read_at']
    
    def get_is_expired(self, obj):
        return obj.is_expired()


class NotificationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for notification list"""
    type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'notification_type', 'type_display',
            'priority', 'priority_display', 'is_read', 'created_at', 'action_url'
        ]


class CreateNotificationSerializer(serializers.ModelSerializer):
    """Serializer for creating notifications"""
    class Meta:
        model = Notification
        fields = [
            'user', 'title', 'message', 'notification_type', 'priority',
            'related_object_type', 'related_object_id', 'action_url', 'expires_at'
        ]


class BulkReadSerializer(serializers.Serializer):
    """Serializer for bulk read operations"""
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for NotificationPreference"""
    user_details = UserSerializer(source='user', read_only=True)
    digest_frequency_display = serializers.CharField(source='get_digest_frequency_display', read_only=True)
    
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'user', 'user_details',
            'email_lease_expiring', 'email_payment_due', 'email_payment_received',
            'email_maintenance_updates', 'email_document_uploaded', 'email_report_ready',
            'app_lease_expiring', 'app_payment_due', 'app_payment_received',
            'app_maintenance_updates', 'app_document_uploaded', 'app_report_ready',
            'digest_frequency', 'digest_frequency_display',
            'quiet_hours_start', 'quiet_hours_end',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """Serializer for NotificationTemplate"""
    type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = NotificationTemplate
        fields = [
            'id', 'name', 'notification_type', 'type_display',
            'title_template', 'message_template',
            'priority', 'priority_display',
            'created_at', 'updated_at'
        ]


class NotificationStatisticsSerializer(serializers.Serializer):
    """Serializer for notification statistics"""
    total_notifications = serializers.IntegerField()
    unread_notifications = serializers.IntegerField()
    read_notifications = serializers.IntegerField()
    by_type = serializers.DictField()
    by_priority = serializers.DictField()
    recent_notifications = serializers.ListField()
