from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Property
from tenants.models import Tenant
from leases.models import Lease

User = get_user_model()


class Revenue(models.Model):
    """Revenue tracking model"""
    
    SOURCE_CHOICES = [
        ('rent', 'Rent'),
        ('late_fee', 'Late Fee'),
        ('security_deposit', 'Security Deposit'),
        ('parking', 'Parking'),
        ('maintenance', 'Maintenance Fee'),
        ('other', 'Other'),
    ]
    
    financial_property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='revenues',
        db_column='property_id'
    )
    lease = models.ForeignKey(
        Lease,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='revenues'
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='revenues'
    )
    
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='rent')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    
    # Payment details
    payment_method = models.CharField(max_length=50, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='revenues_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'revenues'
        ordering = ['-date', '-created_at']
        verbose_name = 'Revenue'
        verbose_name_plural = 'Revenues'
        indexes = [
            models.Index(fields=['financial_property', 'date']),
            models.Index(fields=['tenant', 'date']),
            models.Index(fields=['source']),
        ]
    
    def __str__(self):
        return f"{self.get_source_display()} - ${self.amount} - {self.date}"


class Expense(models.Model):
    """Expense tracking model"""
    
    CATEGORY_CHOICES = [
        ('maintenance', 'Maintenance & Repairs'),
        ('utilities', 'Utilities'),
        ('insurance', 'Insurance'),
        ('property_tax', 'Property Tax'),
        ('management_fee', 'Management Fee'),
        ('mortgage', 'Mortgage Payment'),
        ('hoa', 'HOA Fees'),
        ('marketing', 'Marketing'),
        ('legal', 'Legal Fees'),
        ('supplies', 'Supplies'),
        ('other', 'Other'),
    ]
    
    financial_property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='expenses',
        db_column='property_id'
    )
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    
    # Vendor details
    vendor_name = models.CharField(max_length=200, blank=True)
    invoice_number = models.CharField(max_length=100, blank=True)
    
    # Payment details
    payment_method = models.CharField(max_length=50, blank=True)
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    
    # Attachments
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='expenses_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'expenses'
        ordering = ['-date', '-created_at']
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        indexes = [
            models.Index(fields=['financial_property', 'date']),
            models.Index(fields=['category']),
            models.Index(fields=['paid']),
        ]
    
    def __str__(self):
        return f"{self.get_category_display()} - ${self.amount} - {self.date}"


class Transaction(models.Model):
    """General transaction model for all financial activities"""
    
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    financial_property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='transactions',
        db_column='property_id'
    )
    
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    
    # Links to revenue or expense
    revenue = models.ForeignKey(
        Revenue,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    expense = models.ForeignKey(
        Expense,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'transactions'
        ordering = ['-date', '-created_at']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        indexes = [
            models.Index(fields=['financial_property', 'date']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - ${self.amount} - {self.date}"


class Payment(models.Model):
    """Payment tracking for rent and other charges"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('late', 'Late'),
        ('partial', 'Partially Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    lease = models.ForeignKey(
        Lease,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    financial_property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='payments',
        db_column='property_id'
    )
    
    # Payment details
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Late fees
    late_fee_applied = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Payment method
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-due_date']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        indexes = [
            models.Index(fields=['lease', 'due_date']),
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['financial_property', 'due_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Payment - {self.tenant.get_full_name()} - ${self.amount_due} - {self.due_date}"
    
    def get_balance(self):
        """Calculate remaining balance"""
        return self.amount_due + self.late_fee_applied - self.amount_paid
    
    def is_overdue(self):
        """Check if payment is overdue"""
        from django.utils import timezone
        if self.status in ['paid', 'cancelled']:
            return False
        return self.due_date < timezone.now().date()

