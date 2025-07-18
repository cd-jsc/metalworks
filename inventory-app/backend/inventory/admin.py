from django.contrib import admin
from .models import (
    Category, Tag, Supplier, Warehouse, Location, BinLocation,
    ProductTemplate, ProductVariant, Item, Barcode, Label, Batch, 
    StockLevel, StockMovement, StockReservation, CycleCount, CycleCountItem
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'created_at']
    list_filter = ['parent', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'contact_person', 'email']
    ordering = ['name']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'warehouse_type', 'city', 'manager', 'is_active', 'created_at']
    list_filter = ['warehouse_type', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'address', 'city']
    ordering = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'warehouse', 'location_type', 'parent', 'is_active', 'created_at']
    list_filter = ['warehouse', 'location_type', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'barcode']
    ordering = ['warehouse__name', 'name']


@admin.register(BinLocation)
class BinLocationAdmin(admin.ModelAdmin):
    list_display = ['bin_code', 'location', 'capacity', 'max_weight', 'is_active', 'created_at']
    list_filter = ['location__warehouse', 'is_active', 'created_at']
    search_fields = ['bin_code', 'barcode', 'location__name']
    ordering = ['location__name', 'bin_code']


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ['name', 'variant_code', 'size', 'color', 'cost_price', 'selling_price', 'is_active']


@admin.register(ProductTemplate)
class ProductTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'manufacturer', 'is_active', 'created_at']
    list_filter = ['category', 'brand', 'manufacturer', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'brand', 'manufacturer']
    ordering = ['name']
    filter_horizontal = ['tags']
    inlines = [ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['name', 'template', 'variant_code', 'size', 'color', 'cost_price', 'selling_price', 'is_active']
    list_filter = ['template', 'size', 'color', 'is_active', 'created_at']
    search_fields = ['name', 'variant_code', 'template__name']
    ordering = ['template__name', 'name']


class BarcodeInline(admin.TabularInline):
    model = Barcode
    extra = 0
    fields = ['barcode_type', 'barcode_data', 'is_primary', 'is_active']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category', 'product_variant', 'unit_of_measure', 'cost_price', 'selling_price', 'is_active']
    list_filter = ['category', 'product_variant__template', 'unit_of_measure', 'track_batches', 'track_expiry', 'is_active', 'created_at']
    search_fields = ['sku', 'name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['tags']
    inlines = [BarcodeInline]


@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ['barcode_data', 'item', 'barcode_type', 'is_primary', 'is_active', 'created_at']
    list_filter = ['barcode_type', 'is_primary', 'is_active', 'created_at']
    search_fields = ['barcode_data', 'item__sku', 'item__name']
    ordering = ['item__sku', '-is_primary']


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'label_type', 'width', 'height', 'is_default', 'is_active', 'created_at']
    list_filter = ['label_type', 'is_default', 'is_active', 'created_at']
    search_fields = ['name']
    ordering = ['label_type', 'name']


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['batch_number', 'item', 'supplier', 'quality_status', 'expiry_date', 'is_expired']
    list_filter = ['quality_status', 'supplier', 'expiry_date', 'created_at']
    search_fields = ['batch_number', 'item__sku', 'item__name']
    ordering = ['-created_at']
    readonly_fields = ['is_expired', 'created_at', 'updated_at']


@admin.register(StockLevel)
class StockLevelAdmin(admin.ModelAdmin):
    list_display = ['item', 'warehouse', 'location', 'bin_location', 'batch', 'quantity', 'reserved_quantity', 'available_quantity', 'last_movement']
    list_filter = ['warehouse', 'location', 'item__category', 'last_movement']
    search_fields = ['item__sku', 'item__name', 'warehouse__name', 'location__name']
    ordering = ['item__name', 'warehouse__name', 'location__name']
    readonly_fields = ['available_quantity', 'created_at', 'updated_at']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'movement_type', 'item', 'warehouse', 'location', 'quantity', 'performed_by', 'created_at']
    list_filter = ['movement_type', 'warehouse', 'location', 'performed_by', 'created_at']
    search_fields = ['reference_number', 'item__sku', 'item__name', 'reason']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(StockReservation)
class StockReservationAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'item', 'warehouse', 'location', 'quantity', 'reserved_at', 'expires_at', 'is_active']
    list_filter = ['is_active', 'warehouse', 'location', 'reserved_at']
    search_fields = ['reference_number', 'item__sku', 'item__name']
    ordering = ['-reserved_at']


class CycleCountItemInline(admin.TabularInline):
    model = CycleCountItem
    extra = 0
    readonly_fields = ['variance']
    fields = ['item', 'location', 'bin_location', 'batch', 'system_quantity', 'counted_quantity', 'variance', 'is_counted']


@admin.register(CycleCount)
class CycleCountAdmin(admin.ModelAdmin):
    list_display = ['count_id', 'warehouse', 'location', 'status', 'scheduled_date', 'actual_date', 'assigned_to', 'counted_by']
    list_filter = ['status', 'warehouse', 'location', 'scheduled_date', 'assigned_to']
    search_fields = ['count_id', 'warehouse__name', 'location__name']
    ordering = ['-scheduled_date']
    inlines = [CycleCountItemInline]
    readonly_fields = ['count_id', 'created_at', 'updated_at']


@admin.register(CycleCountItem)
class CycleCountItemAdmin(admin.ModelAdmin):
    list_display = ['cycle_count', 'item', 'location', 'bin_location', 'system_quantity', 'counted_quantity', 'variance', 'is_counted']
    list_filter = ['is_counted', 'cycle_count__status', 'counted_at']
    search_fields = ['item__sku', 'item__name', 'cycle_count__count_id']
    ordering = ['cycle_count', 'item__name']
    readonly_fields = ['variance']