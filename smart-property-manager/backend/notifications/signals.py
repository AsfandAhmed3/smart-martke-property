from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

from leases.models import Lease
from financials.models import Payment
from maintenance.models import MaintenanceRequest
from documents.models import Document
from reports.models import Report
from .models import Notification


@receiver(post_save, sender=Lease)
def notify_lease_expiring(sender, instance, created, **kwargs):
    """
    Create notification when lease is expiring soon (30 days)
    """
    if not created and instance.status == 'expiring_soon':
        # Get all users who should be notified (property owner, managers)
        from users.models import User
        users_to_notify = User.objects.filter(
            role__can_manage_leases=True
        )
        
        for user in users_to_notify:
            # Check if notification already exists
            exists = Notification.objects.filter(
                user=user,
                related_object_type='lease',
                related_object_id=instance.id,
                notification_type='lease_expiring',
                is_read=False
            ).exists()
            
            if not exists:
                Notification.objects.create(
                    user=user,
                    title=f'Lease Expiring Soon: {instance.lease_property.name}',
                    message=f'The lease for {instance.tenant.get_full_name()} at {instance.lease_property.name} will expire on {instance.end_date}.',
                    notification_type='lease_expiring',
                    priority='high',
                    related_object_type='lease',
                    related_object_id=instance.id,
                    action_url=f'/leases/{instance.id}'
                )


@receiver(post_save, sender=Payment)
def notify_payment_status(sender, instance, created, **kwargs):
    """
    Create notification for payment due or overdue
    """
    from users.models import User
    
    if instance.status == 'overdue':
        # Notify managers
        users_to_notify = User.objects.filter(
            role__can_manage_financials=True
        )
        
        for user in users_to_notify:
            exists = Notification.objects.filter(
                user=user,
                related_object_type='payment',
                related_object_id=instance.id,
                notification_type='payment_overdue',
                is_read=False
            ).exists()
            
            if not exists:
                Notification.objects.create(
                    user=user,
                    title=f'Payment Overdue: {instance.description}',
                    message=f'Payment of ${instance.amount_due} is overdue. Due date was {instance.due_date}.',
                    notification_type='payment_overdue',
                    priority='urgent',
                    related_object_type='payment',
                    related_object_id=instance.id,
                    action_url=f'/financials/payments/{instance.id}'
                )
    
    elif instance.status == 'paid' and not created:
        # Notify when payment is received
        users_to_notify = User.objects.filter(
            role__can_manage_financials=True
        )
        
        for user in users_to_notify:
            Notification.objects.create(
                user=user,
                title=f'Payment Received: {instance.description}',
                message=f'Payment of ${instance.amount_paid} has been received.',
                notification_type='payment_received',
                priority='normal',
                related_object_type='payment',
                related_object_id=instance.id,
                action_url=f'/financials/payments/{instance.id}'
            )


@receiver(post_save, sender=MaintenanceRequest)
def notify_maintenance_updates(sender, instance, created, **kwargs):
    """
    Create notification for maintenance request updates
    """
    from users.models import User
    
    if created:
        # Notify superadmins and users with admin roles about new maintenance request
        users_to_notify = User.objects.filter(
            is_superadmin=True
        ) | User.objects.filter(
            role__name__in=['admin', 'portfolio_manager']
        )
        
        priority_map = {
            'emergency': 'urgent',
            'high': 'high',
            'medium': 'normal',
            'low': 'low'
        }
        
        for user in users_to_notify:
            Notification.objects.create(
                user=user,
                title=f'New Maintenance Request: {instance.title}',
                message=f'A new {instance.get_priority_display()} priority maintenance request has been created at {instance.maintenance_property.name}.',
                notification_type='maintenance_created',
                priority=priority_map.get(instance.priority, 'normal'),
                related_object_type='maintenance',
                related_object_id=instance.id,
                action_url=f'/maintenance/{instance.id}'
            )
    
    elif instance.status == 'completed':
        # Notify tenant and managers when completed
        users_to_notify = []
        
        if instance.tenant:
            users_to_notify.append(instance.tenant.tenant_property.owner if hasattr(instance.tenant.tenant_property, 'owner') else None)
        
        if instance.reported_by:
            users_to_notify.append(instance.reported_by)
        
        for user in filter(None, users_to_notify):
            Notification.objects.create(
                user=user,
                title=f'Maintenance Completed: {instance.title}',
                message=f'The maintenance request at {instance.maintenance_property.name} has been completed.',
                notification_type='maintenance_completed',
                priority='normal',
                related_object_type='maintenance',
                related_object_id=instance.id,
                action_url=f'/maintenance/{instance.id}'
            )


@receiver(post_save, sender=Document)
def notify_document_uploaded(sender, instance, created, **kwargs):
    """
    Create notification when document is uploaded
    """
    if created:
        from users.models import User
        
        # Notify users with document management permissions
        users_to_notify = User.objects.filter(
            role__can_edit_properties=True
        )
        
        for user in users_to_notify:
            if user != instance.uploaded_by:  # Don't notify the uploader
                Notification.objects.create(
                    user=user,
                    title=f'New Document: {instance.name}',
                    message=f'A new {instance.get_category_display()} document has been uploaded' + (f' for {instance.document_property.name}' if instance.document_property else '') + '.',
                    notification_type='document_uploaded',
                    priority='low',
                    related_object_type='document',
                    related_object_id=instance.id,
                    action_url=f'/documents/{instance.id}'
                )


@receiver(post_save, sender=Report)
def notify_report_ready(sender, instance, created, **kwargs):
    """
    Create notification when report is ready
    """
    if not created and instance.status == 'completed':
        # Notify the user who created the report
        Notification.objects.create(
            user=instance.created_by,
            title=f'Report Ready: {instance.name}',
            message=f'Your {instance.get_report_type_display()} report is ready for download.',
            notification_type='report_ready',
            priority='normal',
            related_object_type='report',
            related_object_id=instance.id,
            action_url=f'/reports/{instance.id}'
        )
