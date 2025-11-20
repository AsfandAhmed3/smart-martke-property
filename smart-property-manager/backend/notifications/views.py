from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import Notification, NotificationPreference, NotificationTemplate
from .serializers import (
    NotificationSerializer,
    NotificationListSerializer,
    CreateNotificationSerializer,
    BulkReadSerializer,
    NotificationPreferenceSerializer,
    NotificationTemplateSerializer,
    NotificationStatisticsSerializer
)


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for Notification management"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'priority', 'is_read']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'priority']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Users can only see their own notifications
        return Notification.objects.filter(user=self.request.user).select_related('user')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NotificationListSerializer
        elif self.action == 'create':
            return CreateNotificationSerializer
        return NotificationSerializer
    
    def perform_create(self, serializer):
        # Admin/system can create notifications for any user
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications"""
        notifications = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_unread(self, request, pk=None):
        """Mark notification as unread"""
        notification = self.get_object()
        notification.mark_as_unread()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        from django.utils import timezone
        updated_count = self.get_queryset().filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        return Response({
            'message': f'{updated_count} notifications marked as read',
            'count': updated_count
        })
    
    @action(detail=False, methods=['post'])
    def bulk_read(self, request):
        """Mark multiple notifications as read"""
        serializer = BulkReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        notification_ids = serializer.validated_data['notification_ids']
        notifications = self.get_queryset().filter(id__in=notification_ids, is_read=False)
        
        from django.utils import timezone
        updated_count = 0
        for notification in notifications:
            notification.mark_as_read()
            updated_count += 1
        
        return Response({
            'message': f'{updated_count} notifications marked as read',
            'count': updated_count
        })
    
    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """Delete multiple notifications"""
        notification_ids = request.data.get('notification_ids', [])
        
        if not notification_ids:
            return Response(
                {'error': 'notification_ids is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        notifications = self.get_queryset().filter(id__in=notification_ids)
        deleted_count = notifications.count()
        notifications.delete()
        
        return Response({
            'message': f'{deleted_count} notifications deleted',
            'count': deleted_count
        })
    
    @action(detail=False, methods=['delete'])
    def clear_all(self, request):
        """Clear all read notifications"""
        deleted_count = self.get_queryset().filter(is_read=True).delete()[0]
        return Response({
            'message': f'{deleted_count} notifications cleared',
            'count': deleted_count
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get notification statistics"""
        queryset = self.get_queryset()
        
        total_notifications = queryset.count()
        unread_notifications = queryset.filter(is_read=False).count()
        read_notifications = queryset.filter(is_read=True).count()
        
        # Notifications by type
        by_type = {}
        types = queryset.values('notification_type').annotate(count=Count('id'))
        for t in types:
            by_type[t['notification_type']] = t['count']
        
        # Notifications by priority
        by_priority = {}
        priorities = queryset.values('priority').annotate(count=Count('id'))
        for p in priorities:
            by_priority[p['priority']] = p['count']
        
        # Recent notifications
        recent = queryset.order_by('-created_at')[:10]
        recent_notifications = NotificationListSerializer(recent, many=True).data
        
        data = {
            'total_notifications': total_notifications,
            'unread_notifications': unread_notifications,
            'read_notifications': read_notifications,
            'by_type': by_type,
            'by_priority': by_priority,
            'recent_notifications': recent_notifications
        }
        
        serializer = NotificationStatisticsSerializer(data)
        return Response(serializer.data)


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for NotificationPreference management"""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationPreferenceSerializer
    
    def get_queryset(self):
        # Users can only manage their own preferences
        return NotificationPreference.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_preferences(self, request):
        """Get current user's notification preferences"""
        preference, created = NotificationPreference.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(preference)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_preferences(self, request):
        """Update current user's notification preferences"""
        preference, created = NotificationPreference.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(preference, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for NotificationTemplate management (Admin only)"""
    permission_classes = [IsAuthenticated]
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['notification_type', 'priority']
    search_fields = ['name', 'title_template', 'message_template']
    
    @action(detail=True, methods=['post'])
    def test_render(self, request, pk=None):
        """Test render template with sample context"""
        template = self.get_object()
        context = request.data.get('context', {})
        
        try:
            title, message = template.render(context)
            return Response({
                'title': title,
                'message': message
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
