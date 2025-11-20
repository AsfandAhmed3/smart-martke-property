from rest_framework import viewsets, filters, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Revenue, Expense, Transaction, Payment
from .serializers import (
    RevenueSerializer,
    ExpenseSerializer,
    TransactionSerializer,
    PaymentSerializer,
    FinancialStatisticsSerializer,
    PropertyFinancialSummarySerializer,
    MonthlyRevenueSerializer
)


class RevenueViewSet(viewsets.ModelViewSet):
    """ViewSet for Revenue management"""
    permission_classes = [IsAuthenticated]
    queryset = Revenue.objects.select_related('financial_property', 'tenant', 'lease').all()
    serializer_class = RevenueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['financial_property', 'tenant', 'source', 'date']
    search_fields = ['description', 'reference_number', 'tenant__first_name', 'tenant__last_name']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    """ViewSet for Expense management"""
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.select_related('financial_property').all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['financial_property', 'category', 'paid', 'date']
    search_fields = ['description', 'vendor_name', 'invoice_number']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark an expense as paid"""
        expense = self.get_object()
        paid_date = request.data.get('paid_date', timezone.now().date())
        
        expense.paid = True
        expense.paid_date = paid_date
        expense.save()
        
        serializer = self.get_serializer(expense)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for Transaction management"""
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.select_related('financial_property').all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['financial_property', 'transaction_type', 'status', 'date']
    search_fields = ['description', 'category']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for Payment management"""
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.select_related('lease', 'tenant', 'financial_property').all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['financial_property', 'tenant', 'lease', 'status']
    search_fields = ['tenant__first_name', 'tenant__last_name', 'transaction_id']
    ordering_fields = ['due_date', 'amount_due', 'created_at']
    ordering = ['-due_date']
    
    @action(detail=True, methods=['post'])
    def record_payment(self, request, pk=None):
        """Record a payment"""
        payment = self.get_object()
        amount = request.data.get('amount')
        paid_date = request.data.get('paid_date', timezone.now().date())
        payment_method = request.data.get('payment_method', '')
        transaction_id = request.data.get('transaction_id', '')
        
        if not amount:
            return Response(
                {'error': 'Amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.amount_paid += float(amount)
        payment.paid_date = paid_date
        payment.payment_method = payment_method
        payment.transaction_id = transaction_id
        
        # Update status
        if payment.amount_paid >= (payment.amount_due + payment.late_fee_applied):
            payment.status = 'paid'
        elif payment.amount_paid > 0:
            payment.status = 'partial'
        
        payment.save()
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue payments"""
        today = timezone.now().date()
        overdue_payments = self.get_queryset().filter(
            due_date__lt=today,
            status__in=['pending', 'partial']
        )
        
        serializer = self.get_serializer(overdue_payments, many=True)
        return Response(serializer.data)


class AnalyticsView(views.APIView):
    """Analytics and financial statistics"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get overall financial statistics"""
        # Date filtering
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        revenue_qs = Revenue.objects.all()
        expense_qs = Expense.objects.all()
        payment_qs = Payment.objects.all()
        
        if start_date:
            revenue_qs = revenue_qs.filter(date__gte=start_date)
            expense_qs = expense_qs.filter(date__gte=start_date)
            payment_qs = payment_qs.filter(due_date__gte=start_date)
        
        if end_date:
            revenue_qs = revenue_qs.filter(date__lte=end_date)
            expense_qs = expense_qs.filter(date__lte=end_date)
            payment_qs = payment_qs.filter(due_date__lte=end_date)
        
        total_revenue = revenue_qs.aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = expense_qs.aggregate(total=Sum('amount'))['total'] or 0
        net_income = total_revenue - total_expenses
        
        # Payment statistics
        pending_payments = payment_qs.filter(status='pending').count()
        overdue_payments = payment_qs.filter(
            due_date__lt=timezone.now().date(),
            status__in=['pending', 'partial']
        ).count()
        total_pending_amount = payment_qs.filter(
            status__in=['pending', 'partial']
        ).aggregate(
            total=Sum(F('amount_due') + F('late_fee_applied') - F('amount_paid'))
        )['total'] or 0
        
        from properties.models import Property
        total_properties = Property.objects.count()
        avg_revenue = total_revenue / total_properties if total_properties > 0 else 0
        
        data = {
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'net_income': net_income,
            'total_properties': total_properties,
            'average_revenue_per_property': avg_revenue,
            'pending_payments': pending_payments,
            'overdue_payments': overdue_payments,
            'total_pending_amount': total_pending_amount
        }
        
        serializer = FinancialStatisticsSerializer(data)
        return Response(serializer.data)


class PropertyPerformanceView(views.APIView):
    """Property-wise financial performance"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get financial summary for each property"""
        from properties.models import Property
        
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        properties = Property.objects.all()
        results = []
        
        for prop in properties:
            revenue_qs = prop.revenues.all()
            expense_qs = prop.expenses.all()
            
            if start_date:
                revenue_qs = revenue_qs.filter(date__gte=start_date)
                expense_qs = expense_qs.filter(date__gte=start_date)
            
            if end_date:
                revenue_qs = revenue_qs.filter(date__lte=end_date)
                expense_qs = expense_qs.filter(date__lte=end_date)
            
            total_revenue = revenue_qs.aggregate(total=Sum('amount'))['total'] or 0
            total_expenses = expense_qs.aggregate(total=Sum('amount'))['total'] or 0
            net_income = total_revenue - total_expenses
            
            # Calculate ROI
            roi = (net_income / prop.purchase_price * 100) if prop.purchase_price > 0 else 0
            
            results.append({
                'property_id': prop.id,
                'property_name': prop.name,
                'total_revenue': total_revenue,
                'total_expenses': total_expenses,
                'net_income': net_income,
                'roi': round(roi, 2),
                'occupancy_rate': prop.occupancy_rate
            })
        
        serializer = PropertyFinancialSummarySerializer(results, many=True)
        return Response(serializer.data)


class MonthlyRevenueView(views.APIView):
    """Monthly revenue breakdown"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get monthly revenue for the last 12 months"""
        from dateutil.relativedelta import relativedelta
        
        today = timezone.now().date()
        start_date = today - relativedelta(months=12)
        
        results = []
        current_date = start_date
        
        while current_date <= today:
            month_start = current_date.replace(day=1)
            month_end = (month_start + relativedelta(months=1)) - timedelta(days=1)
            
            revenues = Revenue.objects.filter(
                date__gte=month_start,
                date__lte=month_end
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            expenses = Expense.objects.filter(
                date__gte=month_start,
                date__lte=month_end
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            results.append({
                'month': month_start,
                'total_revenue': revenues,
                'total_expenses': expenses,
                'net_income': revenues - expenses
            })
            
            current_date = month_start + relativedelta(months=1)
        
        serializer = MonthlyRevenueSerializer(results, many=True)
        return Response(serializer.data)

