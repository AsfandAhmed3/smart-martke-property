from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    """User roles for RBAC"""
    ADMIN = 'admin'
    PORTFOLIO_MANAGER = 'portfolio_manager'
    VIEW_ONLY = 'view_only'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (PORTFOLIO_MANAGER, 'Portfolio Manager'),
        (VIEW_ONLY, 'View Only'),
    ]
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    # Permissions
    can_create_properties = models.BooleanField(default=False)
    can_edit_properties = models.BooleanField(default=False)
    can_delete_properties = models.BooleanField(default=False)
    can_manage_tenants = models.BooleanField(default=False)
    can_manage_leases = models.BooleanField(default=False)
    can_manage_financials = models.BooleanField(default=False)
    can_manage_users = models.BooleanField(default=False)
    can_view_analytics = models.BooleanField(default=True)
    can_export_reports = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.get_name_display()


class User(AbstractUser):
    """Custom User model with RBAC"""
    email = models.EmailField(_('email address'), unique=True)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        related_name='users'
    )
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Superadmin field (higher than regular admin)
    is_superadmin = models.BooleanField(default=False, help_text='Designates that this user has all permissions including user management.')
    
    # MFA fields
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=32, blank=True)
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    lease_reminders = models.BooleanField(default=True)
    maintenance_alerts = models.BooleanField(default=True)
    payment_notifications = models.BooleanField(default=True)
    
    # Additional fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    def has_permission(self, permission):
        """Check if user has specific permission based on role"""
        # Superadmins have all permissions
        if self.is_superadmin or self.is_superuser:
            return True
        if not self.role:
            return False
        return getattr(self.role, permission, False)
