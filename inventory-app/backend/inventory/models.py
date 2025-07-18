from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Category(models.Model):
    """Product categories for organizing inventory items"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """Suppliers/Vendors for inventory items"""
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Location(models.Model):
    """Storage locations/warehouses"""
    LOCATION_TYPES = [
        ('warehouse', 'Warehouse'),
        ('store', 'Store'),
        ('distribution_center', 'Distribution Center'),
        ('supplier', 'Supplier Location'),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES, default='warehouse')
    address = models.TextField(blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Item(models.Model):
    """Master data for inventory items"""
    UNIT_CHOICES = [
        ('pcs', 'Pieces'),
        ('kg', 'Kilograms'),
        ('lbs', 'Pounds'),
        ('liter', 'Liters'),
        ('gallon', 'Gallons'),
        ('meter', 'Meters'),
        ('feet', 'Feet'),
        ('box', 'Boxes'),
        ('case', 'Cases'),
    ]

    # Basic item information
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Physical attributes
    unit_of_measure = models.CharField(max_length=20, choices=UNIT_CHOICES, default='pcs')
    weight = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    dimensions = models.CharField(max_length=100, blank=True, help_text="L x W x H")
    
    # Pricing
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Inventory control
    minimum_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    maximum_stock = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    reorder_point = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Tracking settings
    track_batches = models.BooleanField(default=False, help_text="Enable batch/lot tracking")
    track_expiry = models.BooleanField(default=False, help_text="Track expiration dates")
    track_serial = models.BooleanField(default=False, help_text="Track serial numbers")
    
    # Status and metadata
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.sku} - {self.name}"

    @property
    def total_quantity(self):
        """Calculate total quantity across all locations"""
        return sum(stock.quantity for stock in self.stock_levels.all())

    @property
    def is_low_stock(self):
        """Check if item is below reorder point"""
        return self.total_quantity <= self.reorder_point


class Batch(models.Model):
    """Batch/Lot tracking for items"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=50)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Dates
    manufactured_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    received_date = models.DateField(auto_now_add=True)
    
    # Quality control
    quality_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('quarantine', 'Quarantine'),
    ], default='pending')
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['item', 'batch_number']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.item.sku} - Batch {self.batch_number}"

    @property
    def is_expired(self):
        """Check if batch is expired"""
        if self.expiry_date:
            from django.utils import timezone
            return timezone.now().date() > self.expiry_date
        return False


class StockLevel(models.Model):
    """Current stock levels for items at specific locations"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stock_levels')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reserved_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Tracking
    last_counted = models.DateTimeField(null=True, blank=True)
    last_movement = models.DateTimeField(auto_now=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['item', 'location', 'batch']
        ordering = ['item__name', 'location__name']

    def __str__(self):
        batch_info = f" - Batch {self.batch.batch_number}" if self.batch else ""
        return f"{self.item.sku} at {self.location.name}: {self.quantity}{batch_info}"

    @property
    def available_quantity(self):
        """Available quantity after reservations"""
        return self.quantity - self.reserved_quantity


class StockMovement(models.Model):
    """Track all stock movements (receipts, issues, transfers, adjustments)"""
    MOVEMENT_TYPES = [
        ('receipt', 'Receipt'),
        ('issue', 'Issue'),
        ('transfer_in', 'Transfer In'),
        ('transfer_out', 'Transfer Out'),
        ('adjustment', 'Adjustment'),
        ('return', 'Return'),
        ('damage', 'Damage'),
        ('cycle_count', 'Cycle Count'),
    ]

    # Movement details
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    reference_number = models.CharField(max_length=50, unique=True)
    
    # Item and location
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='movements')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    
    # Quantities
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Transfer specific fields
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name='outbound_movements')
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name='inbound_movements')
    
    # Metadata
    reason = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.movement_type} - {self.item.sku} - {self.quantity} units"


class StockReservation(models.Model):
    """Reserved stock for orders or other purposes"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reservations')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    reference_number = models.CharField(max_length=50, help_text="Order number or reference")
    
    # Dates
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-reserved_at']

    def __str__(self):
        return f"Reserved: {self.item.sku} - {self.quantity} units"


class CycleCount(models.Model):
    """Cycle counting for inventory accuracy"""
    count_id = models.UUIDField(default=uuid.uuid4, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    # Count details
    scheduled_date = models.DateField()
    actual_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='scheduled')
    
    # Personnel
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    counted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cycle_counts_performed')
    
    # Results
    total_items = models.IntegerField(default=0)
    items_counted = models.IntegerField(default=0)
    discrepancies_found = models.IntegerField(default=0)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"Cycle Count {self.count_id} - {self.location.name}"


class CycleCountItem(models.Model):
    """Individual items in a cycle count"""
    cycle_count = models.ForeignKey(CycleCount, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    
    # Count results
    system_quantity = models.IntegerField(default=0)
    counted_quantity = models.IntegerField(null=True, blank=True)
    variance = models.IntegerField(default=0)
    
    # Status
    is_counted = models.BooleanField(default=False)
    adjustment_created = models.BooleanField(default=False)
    
    notes = models.TextField(blank=True)
    counted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['cycle_count', 'item', 'batch']

    def __str__(self):
        return f"{self.cycle_count.count_id} - {self.item.sku}"

    def save(self, *args, **kwargs):
        if self.counted_quantity is not None:
            self.variance = self.counted_quantity - self.system_quantity
        super().save(*args, **kwargs)