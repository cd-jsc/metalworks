from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Tag, Supplier, Warehouse, Location, BinLocation, 
    ProductTemplate, ProductVariant, Item, Barcode, Label, Batch, 
    StockLevel, StockMovement, StockReservation, CycleCount, CycleCountItem
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.StringRelatedField(many=True, read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'parent_name', 'subcategories', 'created_at', 'updated_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'description', 'created_at', 'updated_at']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_person', 'email', 'phone', 'address', 'is_active', 'created_at', 'updated_at']


class WarehouseSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'code', 'warehouse_type', 'address', 'city', 'state', 'postal_code', 
                 'country', 'manager', 'manager_name', 'is_active', 'created_at', 'updated_at']


class LocationSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    full_location_path = serializers.CharField(read_only=True)
    
    class Meta:
        model = Location
        fields = ['id', 'warehouse', 'warehouse_name', 'name', 'code', 'location_type', 'parent', 
                 'parent_name', 'barcode', 'full_location_path', 'is_active', 'created_at', 'updated_at']


class BinLocationSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    full_bin_path = serializers.CharField(read_only=True)
    
    class Meta:
        model = BinLocation
        fields = ['id', 'location', 'location_name', 'bin_code', 'barcode', 'capacity', 'max_weight', 
                 'full_bin_path', 'is_active', 'created_at', 'updated_at']


class ProductTemplateSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, source='tags'
    )
    variant_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductTemplate
        fields = ['id', 'name', 'description', 'category', 'category_name', 'tags', 'tag_ids', 
                 'brand', 'manufacturer', 'base_unit_of_measure', 'track_batches', 'track_expiry', 
                 'track_serial', 'variant_count', 'is_active', 'created_by', 'created_at', 'updated_at']
    
    def get_variant_count(self, obj):
        return obj.variants.count()


class ProductVariantSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'template', 'template_name', 'name', 'variant_code', 'size', 'color', 
                 'material', 'style', 'weight', 'dimensions', 'cost_price', 'selling_price', 
                 'is_active', 'created_at', 'updated_at']


class BarcodeSerializer(serializers.ModelSerializer):
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    
    class Meta:
        model = Barcode
        fields = ['id', 'item', 'item_sku', 'item_name', 'barcode_type', 'barcode_data', 
                 'is_primary', 'is_active', 'created_at', 'updated_at']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'label_type', 'template', 'width', 'height', 'is_default', 
                 'is_active', 'created_at', 'updated_at']


class BatchSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Batch
        fields = ['id', 'item', 'item_name', 'item_sku', 'batch_number', 'supplier', 'supplier_name', 
                 'manufactured_date', 'expiry_date', 'received_date', 'quality_status', 'is_expired',
                 'notes', 'created_at', 'updated_at']


class StockLevelSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    bin_location_code = serializers.CharField(source='bin_location.bin_code', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    available_quantity = serializers.IntegerField(read_only=True)
    full_location_path = serializers.CharField(read_only=True)
    
    class Meta:
        model = StockLevel
        fields = ['id', 'item', 'item_name', 'item_sku', 'warehouse', 'warehouse_name', 
                 'location', 'location_name', 'bin_location', 'bin_location_code', 
                 'batch', 'batch_number', 'quantity', 'reserved_quantity', 'available_quantity',
                 'full_location_path', 'last_counted', 'last_movement', 'created_at', 'updated_at']


class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    effective_category_name = serializers.CharField(source='effective_category.name', read_only=True)
    product_variant_name = serializers.CharField(source='product_variant.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    total_quantity = serializers.IntegerField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    stock_levels = StockLevelSerializer(many=True, read_only=True)
    barcodes = BarcodeSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    effective_tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, source='tags'
    )
    
    class Meta:
        model = Item
        fields = ['id', 'sku', 'name', 'description', 'product_variant', 'product_variant_name',
                 'category', 'category_name', 'effective_category_name', 'tags', 'tag_ids', 'effective_tags',
                 'unit_of_measure', 'weight', 'dimensions', 'cost_price', 'selling_price',
                 'minimum_stock', 'maximum_stock', 'reorder_point', 'track_batches', 
                 'track_expiry', 'track_serial', 'is_active', 'created_by', 'created_by_name',
                 'total_quantity', 'is_low_stock', 'stock_levels', 'barcodes', 'created_at', 'updated_at']


class StockMovementSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    bin_location_code = serializers.CharField(source='bin_location.bin_code', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    from_warehouse_name = serializers.CharField(source='from_warehouse.name', read_only=True)
    from_location_name = serializers.CharField(source='from_location.name', read_only=True)
    from_bin_location_code = serializers.CharField(source='from_bin_location.bin_code', read_only=True)
    to_warehouse_name = serializers.CharField(source='to_warehouse.name', read_only=True)
    to_location_name = serializers.CharField(source='to_location.name', read_only=True)
    to_bin_location_code = serializers.CharField(source='to_bin_location.bin_code', read_only=True)
    performed_by_name = serializers.CharField(source='performed_by.get_full_name', read_only=True)
    full_location_path = serializers.CharField(read_only=True)
    
    class Meta:
        model = StockMovement
        fields = ['id', 'movement_type', 'reference_number', 'item', 'item_name', 'item_sku',
                 'warehouse', 'warehouse_name', 'location', 'location_name', 'bin_location', 'bin_location_code',
                 'batch', 'batch_number', 'quantity', 'unit_cost', 'from_warehouse', 'from_warehouse_name',
                 'from_location', 'from_location_name', 'from_bin_location', 'from_bin_location_code',
                 'to_warehouse', 'to_warehouse_name', 'to_location', 'to_location_name', 
                 'to_bin_location', 'to_bin_location_code', 'reason', 'notes', 'performed_by', 
                 'performed_by_name', 'full_location_path', 'created_at']


class StockReservationSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    bin_location_code = serializers.CharField(source='bin_location.bin_code', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockReservation
        fields = ['id', 'item', 'item_name', 'item_sku', 'warehouse', 'warehouse_name',
                 'location', 'location_name', 'bin_location', 'bin_location_code',
                 'batch', 'batch_number', 'quantity', 'reference_number', 'reserved_at',
                 'expires_at', 'is_active', 'notes', 'created_by', 'created_by_name']


class CycleCountItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    bin_location_code = serializers.CharField(source='bin_location.bin_code', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    
    class Meta:
        model = CycleCountItem
        fields = ['id', 'item', 'item_name', 'item_sku', 'location', 'location_name',
                 'bin_location', 'bin_location_code', 'batch', 'batch_number',
                 'system_quantity', 'counted_quantity', 'variance', 'is_counted',
                 'adjustment_created', 'notes', 'counted_at']


class CycleCountSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    counted_by_name = serializers.CharField(source='counted_by.get_full_name', read_only=True)
    items = CycleCountItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = CycleCount
        fields = ['id', 'count_id', 'warehouse', 'warehouse_name', 'location', 'location_name', 
                 'scheduled_date', 'actual_date', 'status', 'assigned_to', 'assigned_to_name', 
                 'counted_by', 'counted_by_name', 'total_items', 'items_counted', 'discrepancies_found', 
                 'notes', 'items', 'created_at', 'updated_at']


# Simplified serializers for dropdowns/selections
class CategorySelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color']


class SupplierSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name']


class WarehouseSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'code']


class LocationSelectSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    
    class Meta:
        model = Location
        fields = ['id', 'warehouse', 'warehouse_name', 'name', 'code']


class BinLocationSelectSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = BinLocation
        fields = ['id', 'location', 'location_name', 'bin_code']


class ProductTemplateSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTemplate
        fields = ['id', 'name']


class ProductVariantSelectSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'template', 'template_name', 'name', 'variant_code']


class ItemSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'sku', 'name', 'unit_of_measure']