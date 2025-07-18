# Database Schema Documentation

## Enhanced Entity Relationship Diagram

```
                    ┌─────────────────┐
                    │    Category     │
                    │─────────────────│
                    │ id (PK)         │
                    │ name            │
                    │ description     │
                    │ parent_id (FK)  │
                    │ created_at      │
                    │ updated_at      │
                    └─────────────────┘
                           │
                           │ 1:N
                           ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│      Tag        │       │ProductTemplate  │       │   Warehouse     │
│─────────────────│       │─────────────────│       │─────────────────│
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ name            │       │ name            │       │ name            │
│ color           │       │ description     │       │ code (UNIQUE)   │
│ description     │       │ category_id (FK)│       │ warehouse_type  │
│ created_at      │       │ tags (M2M)      │       │ address         │
│ updated_at      │       │ brand           │       │ city            │
└─────────────────┘       │ manufacturer    │       │ state           │
        │                 │ base_unit       │       │ postal_code     │
        │ M2M              │ track_batches   │       │ country         │
        │                 │ track_expiry    │       │ manager_id (FK) │
        │                 │ track_serial    │       │ is_active       │
        │                 │ is_active       │       │ created_at      │
        │                 │ created_by (FK) │       │ updated_at      │
        │                 │ created_at      │       └─────────────────┘
        │                 │ updated_at      │               │
        │                 └─────────────────┘               │
        │                         │                         │
        │                         │ 1:N                     │ 1:N
        │                         ▼                         ▼
        │                 ┌─────────────────┐       ┌─────────────────┐
        │                 │ProductVariant   │       │    Location     │
        │                 │─────────────────│       │─────────────────│
        │                 │ id (PK)         │       │ id (PK)         │
        │                 │ template_id (FK)│       │ warehouse_id(FK)│
        │                 │ name            │       │ name            │
        │                 │ variant_code    │       │ code            │
        │                 │ size            │       │ location_type   │
        │                 │ color           │       │ parent_id (FK)  │
        │                 │ material        │       │ barcode         │
        │                 │ style           │       │ is_active       │
        │                 │ weight          │       │ created_at      │
        │                 │ dimensions      │       │ updated_at      │
        │                 │ cost_price      │       └─────────────────┘
        │                 │ selling_price   │               │
        │                 │ is_active       │               │ 1:N
        │                 │ created_at      │               ▼
        │                 │ updated_at      │       ┌─────────────────┐
        │                 └─────────────────┘       │  BinLocation    │
        │                         │                 │─────────────────│
        │                         │ 1:N             │ id (PK)         │
        │                         ▼                 │ location_id (FK)│
        │                 ┌─────────────────┐       │ bin_code        │
        │                 │      Item       │       │ barcode         │
        │                 │─────────────────│       │ capacity        │
        │                 │ id (PK)         │       │ max_weight      │
        │                 │ sku (UNIQUE)    │       │ is_active       │
        │                 │ name            │       │ created_at      │
        │                 │ description     │       │ updated_at      │
        │                 │ variant_id (FK) │       └─────────────────┘
        │                 │ category_id (FK)│               │
        │                 │ tags (M2M)      │               │
        │                 │ unit_of_measure │               │
        │                 │ weight          │               │
        │                 │ dimensions      │               │
        │                 │ cost_price      │               │
        │                 │ selling_price   │               │
        │                 │ minimum_stock   │               │
        │                 │ maximum_stock   │               │
        │                 │ reorder_point   │               │
        │                 │ track_batches   │               │
        │                 │ track_expiry    │               │
        │                 │ track_serial    │               │
        │                 │ is_active       │               │
        │                 │ created_by (FK) │               │
        │                 │ created_at      │               │
        │                 │ updated_at      │               │
        │                 └─────────────────┘               │
        │                         │                         │
        │                         │ 1:N                     │
        │                         ▼                         │
        │                 ┌─────────────────┐               │
        │                 │    Barcode      │               │
        │                 │─────────────────│               │
        │                 │ id (PK)         │               │
        │                 │ item_id (FK)    │               │
        │                 │ barcode_type    │               │
        │                 │ barcode_data    │               │
        │                 │ is_primary      │               │
        │                 │ is_active       │               │
        │                 │ created_at      │               │
        │                 │ updated_at      │               │
        │                 └─────────────────┘               │
        │                         │                         │
        │                         │                         │
        │                         ▼                         │
        └─────────────────────────┬─────────────────────────┘
                                  │
                                  ▼
                          ┌─────────────────┐
                          │   StockLevel    │
                          │─────────────────│
                          │ id (PK)         │
                          │ item_id (FK)    │
                          │ warehouse_id(FK)│
                          │ location_id (FK)│
                          │ bin_location(FK)│
                          │ batch_id (FK)   │
                          │ quantity        │
                          │ reserved_qty    │
                          │ last_counted    │
                          │ last_movement   │
                          │ created_at      │
                          │ updated_at      │
                          └─────────────────┘

┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    Supplier     │       │     Batch       │       │     Label       │
│─────────────────│       │─────────────────│       │─────────────────│
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ name            │       │ item_id (FK)    │       │ name            │
│ contact_person  │       │ batch_number    │       │ label_type      │
│ email           │       │ supplier_id (FK)│       │ template        │
│ phone           │       │ manufactured_dt │       │ width           │
│ address         │       │ expiry_date     │       │ height          │
│ is_active       │       │ received_date   │       │ is_default      │
│ created_at      │       │ quality_status  │       │ is_active       │
│ updated_at      │       │ notes           │       │ created_at      │
└─────────────────┘       │ created_at      │       │ updated_at      │
                          │ updated_at      │       └─────────────────┘
                          └─────────────────┘

┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  StockMovement  │       │StockReservation │       │   CycleCount    │
│─────────────────│       │─────────────────│       │─────────────────│
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ movement_type   │       │ item_id (FK)    │       │ count_id (UUID) │
│ reference_number│       │ warehouse_id(FK)│       │ warehouse_id(FK)│
│ item_id (FK)    │       │ location_id (FK)│       │ location_id (FK)│
│ warehouse_id(FK)│       │ bin_location(FK)│       │ scheduled_date  │
│ location_id (FK)│       │ batch_id (FK)   │       │ actual_date     │
│ bin_location(FK)│       │ quantity        │       │ status          │
│ batch_id (FK)   │       │ reference_number│       │ assigned_to (FK)│
│ quantity        │       │ reserved_at     │       │ counted_by (FK) │
│ unit_cost       │       │ expires_at      │       │ total_items     │
│ from_warehouse  │       │ is_active       │       │ items_counted   │
│ from_location   │       └─────────────────┘       │ discrepancies   │
│ from_bin        │                                 │ notes           │
│ to_warehouse    │                                 │ created_by (FK) │
│ to_location     │                                 │ created_at      │
│ to_bin          │                                 │ updated_at      │
│ reason          │                                 └─────────────────┘
│ notes           │                                         │
│ performed_by    │                                         │ 1:N
│ created_at      │                                         ▼
└─────────────────┘                                 ┌─────────────────┐
                                                    │CycleCountItem   │
                                                    │─────────────────│
                                                    │ id (PK)         │
                                                    │ cycle_count (FK)│
                                                    │ item_id (FK)    │
                                                    │ location_id (FK)│
                                                    │ bin_location(FK)│
                                                    │ batch_id (FK)   │
                                                    │ system_quantity │
                                                    │ counted_quantity│
                                                    │ variance        │
                                                    │ is_counted      │
                                                    │ adjustment_made │
                                                    │ notes           │
                                                    │ counted_at      │
                                                    └─────────────────┘
```

## Enhanced Features Summary

### 🏷️ **Tags System**
- **Flexible Classification**: Unlike hierarchical categories, tags provide flexible, multi-dimensional classification
- **Visual Organization**: Color-coded tags for quick visual identification
- **Many-to-Many Relationships**: Items can have multiple tags, tags can be applied to multiple items
- **Template Integration**: Tags can be applied to product templates and inherited by variants

### 🎯 **Product Variants System**
- **Template-Based**: Product templates define common attributes for variant families
- **Variant Attributes**: Size, color, material, style specifications
- **Inheritance**: Variants inherit tracking settings and categories from templates
- **Individual Pricing**: Each variant can have its own cost and selling price
- **SKU Generation**: Automatic or manual SKU assignment for variants

### 🏢 **Enhanced Warehouse Management**
- **Hierarchical Locations**: Warehouse → Location → Bin structure
- **Location Types**: Zones, aisles, racks, shelves, bins, floor storage
- **Barcode Integration**: Scannable barcodes for locations and bins
- **Capacity Management**: Volume and weight capacity tracking for bins
- **Geographic Information**: Full address details for warehouses

### 📊 **Bin Location System**
- **Granular Tracking**: Track inventory down to specific bin locations
- **Capacity Constraints**: Maximum volume and weight limits
- **Barcode Support**: Individual barcodes for each bin location
- **Hierarchical Paths**: Full location paths (Warehouse > Zone > Aisle > Bin)
- **Availability Tracking**: Monitor bin utilization and capacity

### 🔍 **Barcode & Labeling System**
- **Multiple Barcode Types**: EAN-13, EAN-8, UPC, Code 128, Code 39, QR codes
- **Primary Barcode**: Designate primary barcode per item
- **Barcode Generation**: Automatic barcode generation with configurable formats
- **Label Templates**: Customizable label templates for different purposes
- **Print Integration**: Label printing functionality with template support

## Enhanced Data Model Features

### **Improved Stock Tracking**
- **Multi-Dimensional**: Item + Warehouse + Location + Bin + Batch tracking
- **Reservation System**: Enhanced with bin-level reservations
- **Transfer Management**: Detailed transfer tracking between specific locations
- **Movement Audit**: Complete audit trail with source and destination details

### **Advanced Inventory Operations**
- **Cycle Counting**: Warehouse and location-specific cycle counts
- **Barcode Scanning**: Quick item lookup and operations via barcode
- **Label Printing**: On-demand label generation for items and locations
- **Batch Management**: Enhanced batch tracking with quality control

### **Flexible Product Management**
- **Template System**: Manage product families with shared attributes
- **Variant Management**: Handle size, color, material variations
- **Tag Classification**: Multi-dimensional tagging system
- **Inheritance**: Automatic attribute inheritance from templates to variants

This enhanced schema provides a comprehensive foundation for modern inventory management with support for complex product hierarchies, detailed location tracking, barcode integration, and flexible classification systems.