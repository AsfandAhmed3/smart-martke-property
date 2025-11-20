from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta

from properties.models import Property
from tenants.models import Tenant
from leases.models import Lease
from financials.models import Revenue, Expense, Payment, Transaction
from maintenance.models import MaintenanceRequest
from documents.models import Document
from notifications.models import Notification


class DashboardStatisticsView(views.APIView):
    """
    Comprehensive dashboard statistics endpoint
    Aggregates data from all modules with optimized queries
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get dashboard statistics with optional date range filtering
        """
        # Get date range from query params (default to last 30 days)
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # Property Statistics
        properties = Property.objects.all()
        property_stats = {
            'total_properties': properties.count(),
            'total_value': float(properties.aggregate(total=Sum('current_value'))['total'] or 0),
            'total_units': properties.aggregate(total=Sum('total_units'))['total'] or 0,
            'occupied_units': properties.aggregate(total=Sum('occupied_units'))['total'] or 0,
            'average_occupancy': properties.aggregate(avg=Avg('occupancy_rate'))['avg'] or 0,
            'average_roi': properties.aggregate(avg=Avg('roi'))['avg'] or 0,
        }
        
        # Calculate overall occupancy percentage
        if property_stats['total_units'] > 0:
            property_stats['occupancy_percentage'] = round(
                (property_stats['occupied_units'] / property_stats['total_units']) * 100, 2
            )
        else:
            property_stats['occupancy_percentage'] = 0
        
        # Tenant Statistics
        tenants = Tenant.objects.select_related('property')
        tenant_stats = {
            'total_tenants': tenants.count(),
            'active_tenants': tenants.filter(status='active').count(),
            'inactive_tenants': tenants.filter(status='inactive').count(),
            'tenants_with_email': tenants.filter(email__isnull=False).exclude(email='').count(),
            'tenants_with_emergency_contact': tenants.filter(
                emergency_contact_name__isnull=False
            ).exclude(emergency_contact_name='').count(),
        }
        
        # Lease Statistics
        leases = Lease.objects.select_related('lease_property', 'tenant')
        lease_stats = {
            'total_leases': leases.count(),
            'active_leases': leases.filter(status='active').count(),
            'expiring_soon': leases.filter(status='expiring_soon').count(),
            'expired_leases': leases.filter(status='expired').count(),
            'pending_leases': leases.filter(status='pending').count(),
        }
        
        # Calculate upcoming lease expirations (next 30 days)
        upcoming_date = timezone.now().date() + timedelta(days=30)
        lease_stats['expiring_next_30_days'] = leases.filter(
            end_date__lte=upcoming_date,
            end_date__gte=timezone.now().date(),
            status__in=['active', 'expiring_soon']
        ).count()
        
        # Financial Statistics (filtered by date range)
        revenues = Revenue.objects.filter(date__gte=start_date)
        expenses = Expense.objects.filter(date__gte=start_date)
        payments = Payment.objects.all()
        transactions = Transaction.objects.filter(date__gte=start_date)
        
        total_revenue = revenues.aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
        net_income = float(total_revenue) - float(total_expenses)
        
        # Payment statistics
        payment_stats = {
            'total_due': float(payments.aggregate(total=Sum('amount_due'))['total'] or 0),
            'total_paid': float(payments.aggregate(total=Sum('amount_paid'))['total'] or 0),
            'pending_payments': payments.filter(status='pending').count(),
            'overdue_payments': payments.filter(status='overdue').count(),
            'paid_payments': payments.filter(status='paid').count(),
        }
        
        financial_stats = {
            'total_revenue': float(total_revenue),
            'total_expenses': float(total_expenses),
            'net_income': net_income,
            'revenue_count': revenues.count(),
            'expense_count': expenses.count(),
            'transaction_count': transactions.count(),
            'payment_stats': payment_stats,
        }
        
        # Calculate profit margin
        if total_revenue > 0:
            financial_stats['profit_margin'] = round((net_income / float(total_revenue)) * 100, 2)
        else:
            financial_stats['profit_margin'] = 0
        
        # Maintenance Statistics
        maintenance = MaintenanceRequest.objects.select_related(
            'maintenance_property', 'tenant', 'assigned_to'
        )
        maintenance_stats = {
            'total_requests': maintenance.count(),
            'open': maintenance.filter(status='open').count(),
            'in_progress': maintenance.filter(status='in_progress').count(),
            'on_hold': maintenance.filter(status='on_hold').count(),
            'completed': maintenance.filter(status='completed').count(),
            'cancelled': maintenance.filter(status='cancelled').count(),
            'high_priority': maintenance.filter(priority='high').count(),
            'emergency': maintenance.filter(priority='emergency').count(),
        }
        
        # Overdue maintenance
        today = timezone.now().date()
        maintenance_stats['overdue'] = maintenance.filter(
            scheduled_date__lt=today,
            status__in=['open', 'in_progress', 'on_hold']
        ).count()
        
        # Document Statistics
        documents = Document.objects.select_related('document_property', 'uploaded_by')
        document_stats = {
            'total_documents': documents.count(),
            'total_size': documents.aggregate(total=Sum('file_size'))['total'] or 0,
            'recent_uploads': documents.filter(uploaded_at__gte=start_date).count(),
        }
        
        # Notification Statistics
        user_notifications = Notification.objects.filter(user=request.user)
        notification_stats = {
            'total_notifications': user_notifications.count(),
            'unread_count': user_notifications.filter(is_read=False).count(),
            'urgent_count': user_notifications.filter(
                priority='urgent', is_read=False
            ).count(),
        }
        
        # Recent Activities (last 10 activities across all modules)
        recent_activities = []
        
        # Recent properties
        recent_properties = properties.order_by('-created_at')[:3]
        for prop in recent_properties:
            recent_activities.append({
                'type': 'property',
                'action': 'added',
                'title': f'Property Added: {prop.name}',
                'timestamp': prop.created_at,
                'icon': 'building'
            })
        
        # Recent tenants
        recent_tenants = tenants.order_by('-created_at')[:3]
        for tenant in recent_tenants:
            recent_activities.append({
                'type': 'tenant',
                'action': 'added',
                'title': f'Tenant Added: {tenant.get_full_name()}',
                'timestamp': tenant.created_at,
                'icon': 'user'
            })
        
        # Recent leases
        recent_leases = leases.order_by('-created_at')[:3]
        for lease in recent_leases:
            recent_activities.append({
                'type': 'lease',
                'action': 'created',
                'title': f'Lease Created: {lease.lease_property.name}',
                'timestamp': lease.created_at,
                'icon': 'file-text'
            })
        
        # Recent maintenance
        recent_maintenance = maintenance.order_by('-reported_date')[:3]
        for maint in recent_maintenance:
            recent_activities.append({
                'type': 'maintenance',
                'action': 'reported',
                'title': f'Maintenance: {maint.title}',
                'timestamp': maint.reported_date,
                'icon': 'tool'
            })
        
        # Sort by timestamp and limit to 10
        recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
        recent_activities = recent_activities[:10]
        
        # Format timestamps
        for activity in recent_activities:
            activity['timestamp'] = activity['timestamp'].isoformat()
        
        # Quick Stats for Dashboard Cards
        quick_stats = {
            'total_properties': property_stats['total_properties'],
            'total_tenants': tenant_stats['active_tenants'],
            'active_leases': lease_stats['active_leases'],
            'monthly_revenue': financial_stats['total_revenue'],
            'pending_maintenance': maintenance_stats['open'] + maintenance_stats['in_progress'],
            'unread_notifications': notification_stats['unread_count'],
        }
        
        # Trends (compare with previous period)
        previous_start = start_date - timedelta(days=days)
        previous_revenues = Revenue.objects.filter(
            date__gte=previous_start, date__lt=start_date
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        previous_expenses = Expense.objects.filter(
            date__gte=previous_start, date__lt=start_date
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        trends = {
            'revenue_change': self._calculate_change(total_revenue, previous_revenues),
            'expense_change': self._calculate_change(total_expenses, previous_expenses),
        }
        
        # Compile response
        response_data = {
            'date_range': {
                'start_date': start_date.isoformat(),
                'end_date': timezone.now().isoformat(),
                'days': days
            },
            'quick_stats': quick_stats,
            'property_stats': property_stats,
            'tenant_stats': tenant_stats,
            'lease_stats': lease_stats,
            'financial_stats': financial_stats,
            'maintenance_stats': maintenance_stats,
            'document_stats': document_stats,
            'notification_stats': notification_stats,
            'recent_activities': recent_activities,
            'trends': trends,
        }
        
        return Response(response_data)
    
    def _calculate_change(self, current, previous):
        """Calculate percentage change between periods"""
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return round(((float(current) - float(previous)) / float(previous)) * 100, 2)


class PropertyPerformanceView(views.APIView):
    """Get performance metrics for all properties"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        properties = Property.objects.all().order_by('-roi')
        
        performance_data = []
        for prop in properties:
            performance_data.append({
                'id': prop.id,
                'name': prop.name,
                'occupancy_rate': prop.occupancy_rate,
                'roi': prop.roi,
                'monthly_revenue': float(prop.monthly_revenue),
                'monthly_expenses': float(prop.monthly_expenses),
                'net_monthly': float(prop.monthly_revenue - prop.monthly_expenses),
                'total_units': prop.total_units,
                'occupied_units': prop.occupied_units,
            })
        
        return Response({
            'properties': performance_data,
            'total_properties': len(performance_data)
        })
