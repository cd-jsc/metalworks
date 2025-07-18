from django.contrib import admin
from .models import (
    Category, Supplier, Location, Item, Batch, StockLevel, 
    StockMovement, StockReservation, CycleCount, CycleCountItem
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'created_at']
    list_filter = ['parent', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'contact_person', 'email']
    ordering = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'location_type', 'manager', 'is_active', 'created_at']
    list_filter = ['location_type', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'address']
    ordering = ['name']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category', 'unit_of_measure', 'cost_price', 'selling_price', 'is_active']
    list_filter = ['category', 'unit_of_measure', 'track_batches', 'track_expiry', 'is_active', 'created_at']
    search_fields = ['sku', 'name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['batch_number', 'item', 'supplier', 'quality_status', 'expiry_date', 'is_expired']
    list_filter = ['quality_status', 'supplier', 'expiry_date', 'created_at']
    search_fields = ['batch_number', 'item__sku', 'item__name']
    ordering = ['-created_at']
    readonly_fields = ['is_expired', 'created_at', 'updated_at']


@admin.register(StockLevel)
class StockLevelAdmin(admin.ModelAdmin):
    list_display = ['item', 'location', 'batch', 'quantity', 'reserved_quantity', 'available_quantity', 'last_movement']
    list_filter = ['location', 'item__category', 'last_movement']
    search_fields = ['item__sku', 'item__name', 'location__name']
    ordering = ['item__name', 'location__name']
    readonly_fields = ['available_quantity', 'created_at', 'updated_at']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'movement_type', 'item', 'location', 'quantity', 'performed_by', 'created_at']
    list_filter = ['movement_type', 'location', 'performed_by', 'created_at']
    search_fields = ['reference_number', 'item__sku', 'item__name', 'reason']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(StockReservation)
class StockReservationAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'item', 'location', 'quantity', 'reserved_at', 'expires_at', 'is_active']
    list_filter = ['is_active', 'location', 'reserved_at']
    search_fields = ['reference_number', 'item__sku', 'item__name']
    ordering = ['-reserved_at']


class CycleCountItemInline(admin.TabularInline):
    model = CycleCountItem
    extra = 0
    readonly_fields = ['variance']


@admin.register(CycleCount)
class CycleCountAdmin(admin.ModelAdmin):
    list_display = ['count_id', 'location', 'status', 'scheduled_date', 'actual_date', 'assigned_to', 'counted_by']
    list_filter = ['status', 'location', 'scheduled_date', 'assigned_to']
    search_fields = ['count_id', 'location__name']
    ordering = ['-scheduled_date']
    inlines = [CycleCountItemInline]
    readonly_fields = ['count_id', 'created_at', 'updated_at']


@admin.register(CycleCountItem)
class CycleCountItemAdmin(admin.ModelAdmin):
    list_display = ['cycle_count', 'item', 'system_quantity', 'counted_quantity', 'variance', 'is_counted']
    list_filter = ['is_counted', 'cycle_count__status', 'counted_at']
    search_fields = ['item__sku', 'item__name', 'cycle_count__count_id']
    ordering = ['cycle_count', 'item__name']
    readonly_fields = ['variance']