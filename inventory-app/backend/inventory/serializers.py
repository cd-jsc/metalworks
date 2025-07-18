from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Supplier, Location, Item, Batch, StockLevel, 
    StockMovement, StockReservation, CycleCount, CycleCountItem
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


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_person', 'email', 'phone', 'address', 'is_active', 'created_at', 'updated_at']


class LocationSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    
    class Meta:
        model = Location
        fields = ['id', 'name', 'code', 'location_type', 'address', 'manager', 'manager_name', 'is_active', 'created_at', 'updated_at']


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
    location_name = serializers.CharField(source='location.name', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    available_quantity = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = StockLevel
        fields = ['id', 'item', 'item_name', 'item_sku', 'location', 'location_name', 
                 'batch', 'batch_number', 'quantity', 'reserved_quantity', 'available_quantity',
                 'last_counted', 'last_movement', 'created_at', 'updated_at']


class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    total_quantity = serializers.IntegerField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    stock_levels = StockLevelSerializer(many=True, read_only=True)
    
    class Meta:
        model = Item
        fields = ['id', 'sku', 'name', 'description', 'category', 'category_name', 
                 'unit_of_measure', 'weight', 'dimensions', 'cost_price', 'selling_price',
                 'minimum_stock', 'maximum_stock', 'reorder_point', 'track_batches', 
                 'track_expiry', 'track_serial', 'is_active', 'created_by', 'created_by_name',
                 'total_quantity', 'is_low_stock', 'stock_levels', 'created_at', 'updated_at']


class StockMovementSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    from_location_name = serializers.CharField(source='from_location.name', read_only=True)
    to_location_name = serializers.CharField(source='to_location.name', read_only=True)
    performed_by_name = serializers.CharField(source='performed_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = ['id', 'movement_type', 'reference_number', 'item', 'item_name', 'item_sku',
                 'location', 'location_name', 'batch', 'batch_number', 'quantity', 'unit_cost',
                 'from_location', 'from_location_name', 'to_location', 'to_location_name',
                 'reason', 'notes', 'performed_by', 'performed_by_name', 'created_at']


class StockReservationSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockReservation
        fields = ['id', 'item', 'item_name', 'item_sku', 'location', 'location_name',
                 'batch', 'batch_number', 'quantity', 'reference_number', 'reserved_at',
                 'expires_at', 'is_active', 'notes', 'created_by', 'created_by_name']


class CycleCountItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    batch_number = serializers.CharField(source='batch.batch_number', read_only=True)
    
    class Meta:
        model = CycleCountItem
        fields = ['id', 'item', 'item_name', 'item_sku', 'batch', 'batch_number',
                 'system_quantity', 'counted_quantity', 'variance', 'is_counted',
                 'adjustment_created', 'notes', 'counted_at']


class CycleCountSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    counted_by_name = serializers.CharField(source='counted_by.get_full_name', read_only=True)
    items = CycleCountItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = CycleCount
        fields = ['id', 'count_id', 'location', 'location_name', 'scheduled_date', 'actual_date',
                 'status', 'assigned_to', 'assigned_to_name', 'counted_by', 'counted_by_name',
                 'total_items', 'items_counted', 'discrepancies_found', 'notes', 'items',
                 'created_at', 'updated_at']


# Simplified serializers for dropdowns/selections
class CategorySelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SupplierSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name']


class LocationSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'code']


class ItemSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'sku', 'name', 'unit_of_measure']