from django.db import models
from django.utils import timezone
from users.models import User


class Notification(models.Model):
    """Notification model for user notifications"""
    
    TYPE_CHOICES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('lease_expiring', 'Lease Expiring'),
        ('lease_expired', 'Lease Expired'),
        ('payment_due', 'Payment Due'),
        ('payment_overdue', 'Payment Overdue'),
        ('payment_received', 'Payment Received'),
        ('maintenance_created', 'Maintenance Request Created'),
        ('maintenance_updated', 'Maintenance Request Updated'),
        ('maintenance_completed', 'Maintenance Request Completed'),
        ('document_uploaded', 'Document Uploaded'),
        ('report_ready', 'Report Ready'),
        ('tenant_added', 'Tenant Added'),
        ('tenant_updated', 'Tenant Updated'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Recipient
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    
    # Content
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Related objects (generic foreign key could be used for better flexibility)
    related_object_type = models.CharField(max_length=50, blank=True, help_text='e.g., property, lease, payment')
    related_object_id = models.IntegerField(null=True, blank=True)
    
    # Action URL
    action_url = models.CharField(max_length=500, blank=True, help_text='URL to navigate when clicked')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text='Notification expiry time')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['priority']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
    
    def mark_as_unread(self):
        """Mark notification as unread"""
        if self.is_read:
            self.is_read = False
            self.read_at = None
            self.save()
    
    def is_expired(self):
        """Check if notification is expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class NotificationPreference(models.Model):
    """User notification preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')
    
    # Email notifications
    email_lease_expiring = models.BooleanField(default=True)
    email_payment_due = models.BooleanField(default=True)
    email_payment_received = models.BooleanField(default=True)
    email_maintenance_updates = models.BooleanField(default=True)
    email_document_uploaded = models.BooleanField(default=False)
    email_report_ready = models.BooleanField(default=True)
    
    # In-app notifications
    app_lease_expiring = models.BooleanField(default=True)
    app_payment_due = models.BooleanField(default=True)
    app_payment_received = models.BooleanField(default=True)
    app_maintenance_updates = models.BooleanField(default=True)
    app_document_uploaded = models.BooleanField(default=True)
    app_report_ready = models.BooleanField(default=True)
    
    # Notification frequency
    digest_frequency = models.CharField(
        max_length=20,
        choices=[
            ('immediate', 'Immediate'),
            ('hourly', 'Hourly'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
        ],
        default='immediate'
    )
    
    # Quiet hours
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"


class NotificationTemplate(models.Model):
    """Template for notifications"""
    name = models.CharField(max_length=255, unique=True)
    notification_type = models.CharField(max_length=50, choices=Notification.TYPE_CHOICES)
    title_template = models.CharField(max_length=255, help_text='Use {variable} for dynamic content')
    message_template = models.TextField(help_text='Use {variable} for dynamic content')
    priority = models.CharField(max_length=20, choices=Notification.PRIORITY_CHOICES, default='normal')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def render(self, context):
        """Render template with context"""
        title = self.title_template.format(**context)
        message = self.message_template.format(**context)
        return title, message
