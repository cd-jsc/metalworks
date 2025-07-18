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


class Tag(models.Model):
    """Tags for flexible item classification"""
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#3B82F6', help_text="Hex color code for UI display")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
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


class Warehouse(models.Model):
    """Physical warehouse locations"""
    WAREHOUSE_TYPES = [
        ('main', 'Main Warehouse'),
        ('distribution', 'Distribution Center'),
        ('retail', 'Retail Store'),
        ('3pl', 'Third-Party Logistics'),
        ('virtual', 'Virtual Warehouse'),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    warehouse_type = models.CharField(max_length=20, choices=WAREHOUSE_TYPES, default='main')
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Location(models.Model):
    """Storage locations/zones within warehouses"""
    LOCATION_TYPES = [
        ('zone', 'Zone'),
        ('aisle', 'Aisle'),
        ('rack', 'Rack'),
        ('shelf', 'Shelf'),
        ('bin', 'Bin'),
        ('floor', 'Floor'),
    ]

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES, default='zone')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sublocations')
    barcode = models.CharField(max_length=100, blank=True, help_text="Location barcode for scanning")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['warehouse', 'code']
        ordering = ['warehouse__name', 'name']

    def __str__(self):
        return f"{self.warehouse.name} - {self.name} ({self.code})"

    @property
    def full_location_path(self):
        """Get full hierarchical location path"""
        path = [self.name]
        parent = self.parent
        while parent:
            path.append(parent.name)
            parent = parent.parent
        return " > ".join(reversed(path))


class BinLocation(models.Model):
    """Specific bin locations within storage locations"""
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='bins')
    bin_code = models.CharField(max_length=20)
    barcode = models.CharField(max_length=100, blank=True, help_text="Bin barcode for scanning")
    capacity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Capacity in cubic units")
    max_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Maximum weight capacity")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['location', 'bin_code']
        ordering = ['location__name', 'bin_code']

    def __str__(self):
        return f"{self.location.name} - {self.bin_code}"

    @property
    def full_bin_path(self):
        """Get full bin location path"""
        return f"{self.location.full_location_path} > {self.bin_code}"


class ProductTemplate(models.Model):
    """Product template for variants - represents the main product"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    
    # Common attributes for all variants
    base_unit_of_measure = models.CharField(max_length=20, choices=[
        ('pcs', 'Pieces'),
        ('kg', 'Kilograms'),
        ('lbs', 'Pounds'),
        ('liter', 'Liters'),
        ('gallon', 'Gallons'),
        ('meter', 'Meters'),
        ('feet', 'Feet'),
        ('box', 'Boxes'),
        ('case', 'Cases'),
    ], default='pcs')
    
    # Tracking settings
    track_batches = models.BooleanField(default=False, help_text="Enable batch/lot tracking")
    track_expiry = models.BooleanField(default=False, help_text="Track expiration dates")
    track_serial = models.BooleanField(default=False, help_text="Track serial numbers")
    
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """Product variants - specific variations of a product template"""
    template = models.ForeignKey(ProductTemplate, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=200)
    variant_code = models.CharField(max_length=50, help_text="Variant identifier (e.g., size, color)")
    
    # Variant-specific attributes
    size = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    material = models.CharField(max_length=100, blank=True)
    style = models.CharField(max_length=100, blank=True)
    
    # Physical attributes
    weight = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    dimensions = models.CharField(max_length=100, blank=True, help_text="L x W x H")
    
    # Pricing
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['template', 'variant_code']
        ordering = ['template__name', 'name']

    def __str__(self):
        return f"{self.template.name} - {self.name}"


class Item(models.Model):
    """Master data for inventory items - can be standalone or linked to product variant"""
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
    
    # Product variant relationship (optional)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    
    # For standalone items (not variants)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
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

    @property
    def effective_category(self):
        """Get category - from variant's template if available, otherwise direct category"""
        if self.product_variant:
            return self.product_variant.template.category
        return self.category

    @property
    def effective_tags(self):
        """Get tags - from variant's template if available, otherwise direct tags"""
        if self.product_variant:
            return self.product_variant.template.tags.all()
        return self.tags.all()


class Barcode(models.Model):
    """Barcode management for items"""
    BARCODE_TYPES = [
        ('ean13', 'EAN-13'),
        ('ean8', 'EAN-8'),
        ('upc', 'UPC'),
        ('code128', 'Code 128'),
        ('code39', 'Code 39'),
        ('qr', 'QR Code'),
        ('custom', 'Custom'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='barcodes')
    barcode_type = models.CharField(max_length=20, choices=BARCODE_TYPES, default='ean13')
    barcode_data = models.CharField(max_length=200, unique=True)
    is_primary = models.BooleanField(default=False, help_text="Primary barcode for this item")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['item__sku', '-is_primary']

    def __str__(self):
        return f"{self.item.sku} - {self.barcode_data}"

    def save(self, *args, **kwargs):
        # Ensure only one primary barcode per item
        if self.is_primary:
            Barcode.objects.filter(item=self.item, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class Label(models.Model):
    """Label templates and configurations"""
    LABEL_TYPES = [
        ('item', 'Item Label'),
        ('location', 'Location Label'),
        ('bin', 'Bin Label'),
        ('shelf', 'Shelf Label'),
        ('batch', 'Batch Label'),
    ]

    name = models.CharField(max_length=100)
    label_type = models.CharField(max_length=20, choices=LABEL_TYPES)
    template = models.TextField(help_text="Label template in HTML/CSS format")
    width = models.DecimalField(max_digits=5, decimal_places=2, help_text="Label width in inches")
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Label height in inches")
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['label_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.label_type})"


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
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    bin_location = models.ForeignKey(BinLocation, on_delete=models.CASCADE, null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reserved_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Tracking
    last_counted = models.DateTimeField(null=True, blank=True)
    last_movement = models.DateTimeField(auto_now=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['item', 'warehouse', 'location', 'bin_location', 'batch']
        ordering = ['item__name', 'warehouse__name', 'location__name']

    def __str__(self):
        bin_info = f" - {self.bin_location.bin_code}" if self.bin_location else ""
        batch_info = f" - Batch {self.batch.batch_number}" if self.batch else ""
        return f"{self.item.sku} at {self.warehouse.name}/{self.location.name}{bin_info}: {self.quantity}{batch_info}"

    @property
    def available_quantity(self):
        """Available quantity after reservations"""
        return self.quantity - self.reserved_quantity

    @property
    def full_location_path(self):
        """Get full location path including bin"""
        path = f"{self.warehouse.name} > {self.location.full_location_path}"
        if self.bin_location:
            path += f" > {self.bin_location.bin_code}"
        return path


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
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    bin_location = models.ForeignKey(BinLocation, on_delete=models.CASCADE, null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    
    # Quantities
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Transfer specific fields
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True, related_name='outbound_movements')
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name='outbound_movements')
    from_bin_location = models.ForeignKey(BinLocation, on_delete=models.CASCADE, null=True, blank=True, related_name='outbound_movements')
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True, related_name='inbound_movements')
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name='inbound_movements')
    to_bin_location = models.ForeignKey(BinLocation, on_delete=models.CASCADE, null=True, blank=True, related_name='inbound_movements')
    
    # Metadata
    reason = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.movement_type} - {self.item.sku} - {self.quantity} units"

    @property
    def full_location_path(self):
        """Get full location path including bin"""
        path = f"{self.warehouse.name} > {self.location.full_location_path}"
        if self.bin_location:
            path += f" > {self.bin_location.bin_code}"
        return path


class StockReservation(models.Model):
    """Reserved stock for orders or other purposes"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reservations')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    bin_location = models.ForeignKey(BinLocation, on_delete=models.CASCADE, null=True, blank=True)
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
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    
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
        return f"Cycle Count {self.count_id} - {self.warehouse.name}"


class CycleCountItem(models.Model):
    """Individual items in a cycle count"""
    cycle_count = models.ForeignKey(CycleCount, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    bin_location = models.ForeignKey(BinLocation, on_delete=models.CASCADE, null=True, blank=True)
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
        unique_together = ['cycle_count', 'item', 'location', 'bin_location', 'batch']

    def __str__(self):
        return f"{self.cycle_count.count_id} - {self.item.sku}"

    def save(self, *args, **kwargs):
        if self.counted_quantity is not None:
            self.variance = self.counted_quantity - self.system_quantity
        super().save(*args, **kwargs)