from rest_framework import serializers
from .models import Revenue, Expense, Transaction, Payment
from properties.serializers import PropertyListSerializer
from tenants.serializers import TenantListSerializer


class RevenueSerializer(serializers.ModelSerializer):
    property_details = PropertyListSerializer(source='financial_property', read_only=True)
    tenant_details = TenantListSerializer(source='tenant', read_only=True)
    source_display = serializers.CharField(source='get_source_display', read_only=True)
    property_name = serializers.CharField(source='financial_property.name', read_only=True)
    tenant_name = serializers.CharField(source='tenant.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = Revenue
        fields = [
            'id', 'financial_property', 'property_name', 'property_details',
            'lease', 'tenant', 'tenant_name', 'tenant_details',
            'source', 'source_display', 'amount', 'date', 'description',
            'payment_method', 'reference_number', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']


class ExpenseSerializer(serializers.ModelSerializer):
    property_details = PropertyListSerializer(source='financial_property', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    property_name = serializers.CharField(source='financial_property.name', read_only=True)
    balance = serializers.SerializerMethodField()
    
    class Meta:
        model = Expense
        fields = [
            'id', 'financial_property', 'property_name', 'property_details',
            'category', 'category_display', 'amount', 'date', 'description',
            'vendor_name', 'invoice_number', 'payment_method',
            'paid', 'paid_date', 'balance', 'receipt',
            'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def get_balance(self, obj):
        return 0 if obj.paid else obj.amount


class TransactionSerializer(serializers.ModelSerializer):
    property_details = PropertyListSerializer(source='financial_property', read_only=True)
    type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    property_name = serializers.CharField(source='financial_property.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'financial_property', 'property_name', 'property_details',
            'transaction_type', 'type_display', 'amount', 'date',
            'description', 'category', 'status', 'status_display',
            'revenue', 'expense', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']


class PaymentSerializer(serializers.ModelSerializer):
    tenant_details = TenantListSerializer(source='tenant', read_only=True)
    property_details = PropertyListSerializer(source='financial_property', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tenant_name = serializers.CharField(source='tenant.get_full_name', read_only=True)
    property_name = serializers.CharField(source='financial_property.name', read_only=True)
    balance = serializers.DecimalField(source='get_balance', max_digits=10, decimal_places=2, read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'lease', 'tenant', 'tenant_name', 'tenant_details',
            'financial_property', 'property_name', 'property_details',
            'amount_due', 'amount_paid', 'due_date', 'paid_date',
            'status', 'status_display', 'late_fee_applied', 'balance',
            'payment_method', 'transaction_id', 'notes', 'is_overdue',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class FinancialStatisticsSerializer(serializers.Serializer):
    """Serializer for financial statistics"""
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_properties = serializers.IntegerField()
    average_revenue_per_property = serializers.DecimalField(max_digits=12, decimal_places=2)
    pending_payments = serializers.IntegerField()
    overdue_payments = serializers.IntegerField()
    total_pending_amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class PropertyFinancialSummarySerializer(serializers.Serializer):
    """Serializer for property financial summary"""
    property_id = serializers.IntegerField()
    property_name = serializers.CharField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    roi = serializers.DecimalField(max_digits=5, decimal_places=2)
    occupancy_rate = serializers.DecimalField(max_digits=5, decimal_places=2)


class MonthlyRevenueSerializer(serializers.Serializer):
    """Serializer for monthly revenue breakdown"""
    month = serializers.DateField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_income = serializers.DecimalField(max_digits=12, decimal_places=2)
