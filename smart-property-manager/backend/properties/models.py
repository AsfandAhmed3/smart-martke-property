from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Owner(models.Model):
    """Property owner/investor model"""
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_properties'
    )
    
    class Meta:
        db_table = 'owners'
        verbose_name = 'Owner'
        verbose_name_plural = 'Owners'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Property(models.Model):
    """Real estate property model"""
    PROPERTY_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed', 'Mixed Use'),
        ('industrial', 'Industrial'),
        ('land', 'Land'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('under_contract', 'Under Contract'),
        ('sold', 'Sold'),
        ('inactive', 'Inactive'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        default='residential'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    
    # Address Information
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='USA')
    
    # Property Details
    total_units = models.IntegerField(default=1)
    occupied_units = models.IntegerField(default=0)
    size_sqft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    
    # Financial Information
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    monthly_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monthly_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Relationships
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='properties'
    )
    
    # Additional Information
    description = models.TextField(blank=True)
    features = models.JSONField(default=dict, blank=True)
    image_url = models.URLField(blank=True)
    
    # Timestamps
    acquisition_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_properties'
    )
    
    class Meta:
        db_table = 'properties'
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def occupancy_rate(self):
        """Calculate occupancy rate percentage"""
        if self.total_units == 0:
            return 0
        return round((self.occupied_units / self.total_units) * 100, 1)
    
    @property
    def roi(self):
        """Calculate Return on Investment percentage"""
        if not self.purchase_price or self.purchase_price == 0:
            return 0
        annual_income = (self.monthly_revenue - self.monthly_expenses) * 12
        return round((annual_income / self.purchase_price) * 100, 1)
    
    @property
    def full_address(self):
        """Get formatted full address"""
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"
