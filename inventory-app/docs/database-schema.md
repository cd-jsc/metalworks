# Database Schema Documentation

## Entity Relationship Diagram

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
│    Supplier     │       │      Item       │       │    Location     │
│─────────────────│       │─────────────────│       │─────────────────│
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ name            │       │ sku (UNIQUE)    │       │ name            │
│ contact_person  │       │ name            │       │ code (UNIQUE)   │
│ email           │       │ description     │       │ location_type   │
│ phone           │       │ category_id (FK)│       │ address         │
│ address         │       │ unit_of_measure │       │ manager_id (FK) │
│ is_active       │       │ weight          │       │ is_active       │
│ created_at      │       │ dimensions      │       │ created_at      │
│ updated_at      │       │ cost_price      │       │ updated_at      │
└─────────────────┘       │ selling_price   │       └─────────────────┘
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
        │ 1:N                     │ 1:N                     │
        ▼                         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     Batch       │       │   StockLevel    │       │  StockMovement  │
│─────────────────│       │─────────────────│       │─────────────────│
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ item_id (FK)    │       │ item_id (FK)    │       │ movement_type   │
│ batch_number    │       │ location_id (FK)│       │ reference_number│
│ supplier_id (FK)│       │ batch_id (FK)   │       │ item_id (FK)    │
│ manufactured_dt │       │ quantity        │       │ location_id (FK)│
│ expiry_date     │       │ reserved_qty    │       │ batch_id (FK)   │
│ received_date   │       │ last_counted    │       │ quantity        │
│ quality_status  │       │ last_movement   │       │ unit_cost       │
│ notes           │       │ created_at      │       │ from_location   │
│ created_at      │       │ updated_at      │       │ to_location     │
│ updated_at      │       └─────────────────┘       │ reason          │
└─────────────────┘                                 │ notes           │
        │                                           │ performed_by    │
        │                                           │ created_at      │
        │                                           └─────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────┐
│StockReservation │
│─────────────────│
│ id (PK)         │
│ item_id (FK)    │
│ location_id (FK)│
│ batch_id (FK)   │
│ quantity        │
│ reference_number│
│ reserved_at     │
│ expires_at      │
│ is_active       │
│ notes           │
│ created_by (FK) │
└─────────────────┘

┌─────────────────┐       ┌─────────────────┐
│   CycleCount    │       │CycleCountItem   │
│─────────────────│       │─────────────────│
│ id (PK)         │       │ id (PK)         │
│ count_id (UUID) │       │ cycle_count (FK)│
│ location_id (FK)│       │ item_id (FK)    │
│ scheduled_date  │       │ batch_id (FK)   │
│ actual_date     │       │ system_quantity │
│ status          │       │ counted_quantity│
│ assigned_to (FK)│       │ variance        │
│ counted_by (FK) │       │ is_counted      │
│ total_items     │       │ adjustment_made │
│ items_counted   │       │ notes           │
│ discrepancies   │       │ counted_at      │
│ notes           │       └─────────────────┘
│ created_at      │               │
│ updated_at      │               │
└─────────────────┘               │
        │                         │
        │ 1:N                     │
        └─────────────────────────┘
```

## Table Definitions

### Core Master Data Tables

#### Category
Hierarchical categorization of inventory items.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Unique identifier |
| name | CharField(100) | UNIQUE, NOT NULL | Category name |
| description | TextField | NULL | Category description |
| parent_id | ForeignKey | NULL, REFERENCES category(id) | Parent category for hierarchy |
| created_at | DateTimeField | NOT NULL | Record creation timestamp |
| updated_at | DateTimeField | NOT NULL | Record update timestamp |

**Indexes:**
- `idx_category_name` on `name`
- `idx_category_parent` on `parent_id`

#### Supplier
Vendor and supplier information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Unique identifier |
| name | CharField(200) | NOT NULL | Supplier name |
| contact_person | CharField(100) | NULL | Contact person name |
| email | EmailField | NULL | Email address |
| phone | CharField(20) | NULL | Phone number |
| address | TextField | NULL | Physical address |
| is_active | BooleanField | DEFAULT TRUE | Active status |
| created_at | DateTimeField | NOT NULL | Record creation timestamp |
| updated_at | DateTimeField | NOT NULL | Record update timestamp |

**Indexes:**
- `idx_supplier_name` on `name`
- `idx_supplier_active` on `is_active`

#### Location
Storage locations and warehouses.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Unique identifier |
| name | CharField(100) | NOT NULL | Location name |
| code | CharField(20) | UNIQUE, NOT NULL | Location code |
| location_type | CharField(20) | NOT NULL | Type of location |
| address | TextField | NULL | Physical address |
| manager_id | ForeignKey | NULL, REFERENCES auth_user(id) | Location manager |
| is_active | BooleanField | DEFAULT TRUE | Active status |
| created_at | DateTimeField | NOT NULL | Record creation timestamp |
| updated_at | DateTimeField | NOT NULL | Record update timestamp |

**Indexes:**
- `idx_location_code` on `code`
- `idx_location_type` on `location_type`
- `idx_location_active` on `is_active`

#### Item
Master item data with all specifications.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Unique identifier |
| sku | CharField(50) | UNIQUE, NOT NULL | Stock Keeping Unit |
| name | CharField(200) | NOT NULL | Item name |
| description | TextField | NULL | Item description |
| category_id | ForeignKey | NULL, REFERENCES category(id) | Item category |
| unit_of_measure | CharField(20) | NOT NULL | Unit of measurement |
| weight | DecimalField(10,3) | NULL | Item weight |
| dimensions | CharField(100) | NULL | Item dimensions |
| cost_price | DecimalField(10,2) | NULL | Cost price |
| selling_price | DecimalField(10,2) | NULL | Selling price |
| minimum_stock | IntegerField | DEFAULT 0 | Minimum stock level |
| maximum_stock | IntegerField | NULL | Maximum stock level |
| reorder_point | IntegerField | DEFAULT 0 | Reorder point |
| track_batches | BooleanField | DEFAULT FALSE | Enable batch tracking |
| track_expiry | BooleanField | DEFAULT FALSE | Enable expiry tracking |
| track_serial | BooleanField | DEFAULT FALSE | Enable serial tracking |
| is_active | BooleanField | DEFAULT TRUE | Active status |
| created_by | ForeignKey | NULL, REFERENCES auth_user(id) | Created by user |
| created_at | DateTimeField | NOT NULL | Record creation timestamp |
| updated_at | DateTimeField | NOT NULL | Record update timestamp |

**Indexes:**
- `idx_item_sku` on `sku`
- `idx_item_name` on `name`
- `idx_item_category` on `category_id`
- `idx_item_active` on `is_active`

### Stock Management Tables

#### Batch
Batch/lot tracking information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Unique identifier |
| item_id | ForeignKey | NOT NULL, REFERENCES item(id) | Associated item |
| batch_number | CharField(50) | NOT NULL | Batch number |
| supplier_id | ForeignKey | NULL, REFERENCES supplier(id) | Supplier |
| manufactured_date | DateField | NULL | Manufacturing date |
| expiry_date | DateField | NULL | Expiry date |
| received_date | DateField | NOT NULL | Received date |
| quality_status | CharField(20) | NOT NULL | Quality status |
| notes | TextField | NULL | Additional notes |
| created_at | DateTimeField | NOT NULL | Record creation timestamp |
| updated_at | DateTimeField | NOT NULL | Record update timestamp |

**Constraints:**
- `UNIQUE(item_id, batch_number)`

**Indexes:**
- `idx_batch_item` on `item_id`
- `idx_batch_number` on `batch_number`
- `idx_batch_expiry` on `expiry_date`
- `idx_batch_quality` on `quality_status`

#### StockLevel
Current stock levels by item and location.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Unique identifier |
| item_id | ForeignKey | NOT NULL, REFERENCES item(id) | Associated item |
| location_id | ForeignKey | NOT NULL, REFERENCES location(id) | Storage location |
| batch_id | ForeignKey | NULL, REFERENCES batch(id) | Associated batch |
| quantity | IntegerField | NOT NULL, >= 0 | Current quantity |
| reserved_quantity | IntegerField | NOT NULL, >= 0 | Reserved quantity |
| last_counted | DateTimeField | NULL | Last count date |
| last_movement | DateTimeField | NOT NULL | Last movement date |
| created_at | DateTimeField | NOT NULL | Record creation timestamp |
| updated_at | DateTimeField | NOT NULL | Record update timestamp |

**Constraints:**
- `UNIQUE(item_id, location_id, batch_id)`

**Indexes:**
- `idx_stock_item_location` on `(item_id, location_id)`
- `idx_stock_location` on `location_id`
- `idx_stock_batch` on `batch_id`
- `idx_stock_movement` on `last_movement`

#### StockMovement
Audit trail of all stock movements.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Unique identifier |
| movement_type | CharField(20) | NOT NULL | Type of movement |
| reference_number | CharField(50) | UNIQUE, NOT NULL | Reference number |
| item_id | ForeignKey | NOT NULL, REFERENCES item(id) | Associated item |
| location_id | ForeignKey | NOT NULL, REFERENCES location(id) | Location |
| batch_id | ForeignKey | NULL, REFERENCES batch(id) | Associated batch |
| quantity | IntegerField | NOT NULL, > 0 | Movement quantity |
| unit_cost | DecimalField(10,2) | NULL | Unit cost |
| from_location_id | ForeignKey | NULL, REFERENCES location(id) | Source location |
| to_location_id | ForeignKey | NULL, REFERENCES location(id) | Destination location |
| reason | CharField(100) | NULL | Movement reason |
| notes | TextField | NULL | Additional notes |
| performed_by | ForeignKey | NULL, REFERENCES auth_user(id) | User who performed |
| created_at | DateTimeField | NOT NULL | Movement timestamp |

**Indexes:**
- `idx_movement_type` on `movement_type`
- `idx_movement_item` on `item_id`
- `idx_movement_location` on `location_id`
- `idx_movement_created` on `created_at`
- `idx_movement_reference` on `reference_number`

#### StockReservation
Reserved stock for orders and allocations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Unique identifier |
| item_id | ForeignKey | NOT NULL, REFERENCES item(id) | Associated item |
| location_id | ForeignKey | NOT NULL, REFERENCES location(id) | Location |
| batch_id | ForeignKey | NULL, REFERENCES batch(id) | Associated batch |
| quantity | IntegerField | NOT NULL, > 0 | Reserved quantity |
| reference_number | CharField(50) | NOT NULL | Order/reference number |
| reserved_at | DateTimeField | NOT NULL | Reservation timestamp |
| expires_at | DateTimeField | NULL | Expiration timestamp |
| is_active | BooleanField | DEFAULT TRUE | Active status |
| notes | TextField | NULL | Additional notes |
| created_by | ForeignKey | NULL, REFERENCES auth_user(id) | Created by user |

**Indexes:**
- `idx_reservation_item` on `item_id`
- `idx_reservation_location` on `location_id`
- `idx_reservation_active` on `is_active`
- `idx_reservation_expires` on `expires_at`

### Cycle Counting Tables

#### CycleCount
Cycle count sessions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Unique identifier |
| count_id | UUIDField | UNIQUE, NOT NULL | Unique count identifier |
| location_id | ForeignKey | NOT NULL, REFERENCES location(id) | Location to count |
| scheduled_date | DateField | NOT NULL | Scheduled date |
| actual_date | DateField | NULL | Actual count date |
| status | CharField(20) | NOT NULL | Count status |
| assigned_to | ForeignKey | NULL, REFERENCES auth_user(id) | Assigned user |
| counted_by | ForeignKey | NULL, REFERENCES auth_user(id) | User who counted |
| total_items | IntegerField | DEFAULT 0 | Total items to count |
| items_counted | IntegerField | DEFAULT 0 | Items counted |
| discrepancies_found | IntegerField | DEFAULT 0 | Discrepancies found |
| notes | TextField | NULL | Additional notes |
| created_at | DateTimeField | NOT NULL | Record creation timestamp |
| updated_at | DateTimeField | NOT NULL | Record update timestamp |

**Indexes:**
- `idx_cycle_count_location` on `location_id`
- `idx_cycle_count_status` on `status`
- `idx_cycle_count_scheduled` on `scheduled_date`

#### CycleCountItem
Individual items in a cycle count.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BigAutoField | PRIMARY KEY | Unique identifier |
| cycle_count_id | ForeignKey | NOT NULL, REFERENCES cyclecount(id) | Cycle count session |
| item_id | ForeignKey | NOT NULL, REFERENCES item(id) | Item being counted |
| batch_id | ForeignKey | NULL, REFERENCES batch(id) | Associated batch |
| system_quantity | IntegerField | DEFAULT 0 | System quantity |
| counted_quantity | IntegerField | NULL | Counted quantity |
| variance | IntegerField | DEFAULT 0 | Variance |
| is_counted | BooleanField | DEFAULT FALSE | Counted status |
| adjustment_created | BooleanField | DEFAULT FALSE | Adjustment created |
| notes | TextField | NULL | Count notes |
| counted_at | DateTimeField | NULL | Count timestamp |

**Constraints:**
- `UNIQUE(cycle_count_id, item_id, batch_id)`

**Indexes:**
- `idx_cycle_item_count` on `cycle_count_id`
- `idx_cycle_item_item` on `item_id`
- `idx_cycle_item_counted` on `is_counted`

## Business Rules & Constraints

### Data Integrity Rules

1. **Stock Levels**
   - Quantity cannot be negative
   - Reserved quantity cannot exceed available quantity
   - Stock levels are automatically updated by movements

2. **Stock Movements**
   - Reference numbers must be unique
   - Quantity must be positive
   - Transfer movements require both from and to locations

3. **Batch Tracking**
   - Batch numbers must be unique per item
   - Expiry dates must be after manufacturing dates
   - Quality status must be valid

4. **Cycle Counting**
   - Count items cannot be modified after count completion
   - Variance is automatically calculated
   - Only one active count per location at a time

### Calculated Fields

1. **Item.total_quantity**: Sum of all stock levels for the item
2. **Item.is_low_stock**: True if total quantity <= reorder point
3. **StockLevel.available_quantity**: quantity - reserved_quantity
4. **Batch.is_expired**: True if expiry_date < current_date
5. **CycleCountItem.variance**: counted_quantity - system_quantity

### Triggers and Procedures

```sql
-- Update stock levels on movement
CREATE OR REPLACE FUNCTION update_stock_on_movement()
RETURNS TRIGGER AS $$
BEGIN
    -- Update stock levels based on movement type
    -- Implementation would handle different movement types
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Calculate variance on cycle count update
CREATE OR REPLACE FUNCTION calculate_count_variance()
RETURNS TRIGGER AS $$
BEGIN
    NEW.variance := COALESCE(NEW.counted_quantity, 0) - NEW.system_quantity;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

## Performance Optimization

### Indexing Strategy

1. **Primary Operations**
   - Fast item lookups by SKU
   - Quick stock level queries by item/location
   - Efficient movement history retrieval

2. **Reporting Queries**
   - Stock summary by location
   - Low stock item identification
   - Expiring batch detection

3. **Composite Indexes**
   - `(item_id, location_id)` for stock queries
   - `(expiry_date, quality_status)` for batch monitoring
   - `(movement_type, created_at)` for movement analysis

### Partitioning Strategy

For high-volume deployments:

```sql
-- Partition stock movements by month
CREATE TABLE stock_movements_y2024m01 PARTITION OF stock_movements
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Partition cycle count items by count
CREATE TABLE cycle_count_items_active PARTITION OF cycle_count_items
FOR VALUES WHERE (is_counted = false);
```

This schema provides a robust foundation for comprehensive inventory management with full traceability, batch tracking, and cycle counting capabilities.