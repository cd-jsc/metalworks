#!/usr/bin/env python3
"""
Dummy Data Generation Script for Inventory Management System
This script generates realistic sample data for testing and demonstration purposes.
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta, date
from decimal import Decimal
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from django.contrib.auth.models import User
from inventory.models import (
    Category, Tag, Supplier, Warehouse, Location, BinLocation,
    ProductTemplate, ProductVariant, Item, Barcode, Label, Batch,
    StockLevel, StockMovement, StockReservation, CycleCount, CycleCountItem
)

def create_categories():
    """Create product categories with hierarchical structure"""
    print("📦 Creating categories...")
    
    categories_data = [
        {"name": "Electronics", "description": "Electronic devices and components"},
        {"name": "Office Supplies", "description": "General office and stationery items"},
        {"name": "Industrial Equipment", "description": "Heavy machinery and industrial tools"},
        {"name": "Raw Materials", "description": "Base materials for manufacturing"},
        {"name": "Finished Goods", "description": "Ready-to-sell products"},
        {"name": "Chemicals", "description": "Chemical products and compounds"},
        {"name": "Textiles", "description": "Fabric and textile materials"},
        {"name": "Food & Beverages", "description": "Consumable food and drink items"},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={"description": cat_data["description"]}
        )
        categories.append(category)
        if created:
            print(f"  ✅ Created category: {category.name}")
    
    # Create subcategories
    subcategories_data = [
        {"name": "Computers", "parent": "Electronics"},
        {"name": "Mobile Devices", "parent": "Electronics"},
        {"name": "Cables & Accessories", "parent": "Electronics"},
        {"name": "Pens & Pencils", "parent": "Office Supplies"},
        {"name": "Paper Products", "parent": "Office Supplies"},
        {"name": "Power Tools", "parent": "Industrial Equipment"},
        {"name": "Safety Equipment", "parent": "Industrial Equipment"},
        {"name": "Steel", "parent": "Raw Materials"},
        {"name": "Plastics", "parent": "Raw Materials"},
    ]
    
    for subcat_data in subcategories_data:
        parent = Category.objects.get(name=subcat_data["parent"])
        subcategory, created = Category.objects.get_or_create(
            name=subcat_data["name"],
            defaults={"parent": parent}
        )
        categories.append(subcategory)
        if created:
            print(f"  ✅ Created subcategory: {subcategory.name}")
    
    return categories

def create_tags():
    """Create tags for flexible item classification"""
    print("🏷️  Creating tags...")
    
    tags_data = [
        {"name": "High Value", "color": "#DC2626", "description": "Items with high monetary value"},
        {"name": "Fragile", "color": "#F59E0B", "description": "Items requiring careful handling"},
        {"name": "Hazardous", "color": "#EF4444", "description": "Items requiring special safety measures"},
        {"name": "Fast Moving", "color": "#10B981", "description": "Items with high turnover rate"},
        {"name": "Seasonal", "color": "#8B5CF6", "description": "Items with seasonal demand"},
        {"name": "Bulk Only", "color": "#6B7280", "description": "Items sold only in bulk quantities"},
        {"name": "Temperature Controlled", "color": "#3B82F6", "description": "Items requiring temperature control"},
        {"name": "Expirable", "color": "#F97316", "description": "Items with expiration dates"},
        {"name": "Serialized", "color": "#06B6D4", "description": "Items tracked by serial number"},
        {"name": "Made to Order", "color": "#84CC16", "description": "Items manufactured on demand"},
    ]
    
    tags = []
    for tag_data in tags_data:
        tag, created = Tag.objects.get_or_create(
            name=tag_data["name"],
            defaults={
                "color": tag_data["color"],
                "description": tag_data["description"]
            }
        )
        tags.append(tag)
        if created:
            print(f"  ✅ Created tag: {tag.name}")
    
    return tags

def create_suppliers():
    """Create supplier records"""
    print("🏢 Creating suppliers...")
    
    suppliers_data = [
        {
            "name": "TechCorp Solutions",
            "contact_person": "John Smith",
            "email": "john.smith@techcorp.com",
            "phone": "+1-555-0101",
            "address": "123 Technology Blvd, Silicon Valley, CA 94025"
        },
        {
            "name": "Industrial Supply Co.",
            "contact_person": "Sarah Johnson",
            "email": "sarah@industrialsupply.com",
            "phone": "+1-555-0102",
            "address": "456 Industrial Ave, Detroit, MI 48201"
        },
        {
            "name": "Global Materials Ltd.",
            "contact_person": "Michael Chen",
            "email": "m.chen@globalmaterials.com",
            "phone": "+1-555-0103",
            "address": "789 Import Street, Los Angeles, CA 90210"
        },
        {
            "name": "Office Express",
            "contact_person": "Lisa Williams",
            "email": "lisa@officeexpress.com",
            "phone": "+1-555-0104",
            "address": "321 Business Park, Chicago, IL 60601"
        },
        {
            "name": "ChemTech Industries",
            "contact_person": "Robert Davis",
            "email": "r.davis@chemtech.com",
            "phone": "+1-555-0105",
            "address": "654 Chemical Row, Houston, TX 77001"
        },
    ]
    
    suppliers = []
    for supplier_data in suppliers_data:
        supplier, created = Supplier.objects.get_or_create(
            name=supplier_data["name"],
            defaults=supplier_data
        )
        suppliers.append(supplier)
        if created:
            print(f"  ✅ Created supplier: {supplier.name}")
    
    return suppliers

def create_warehouses_and_locations():
    """Create warehouses with hierarchical location structure"""
    print("🏭 Creating warehouses and locations...")
    
    # Create admin user for warehouse manager
    admin_user = User.objects.get(username='admin')
    
    warehouses_data = [
        {
            "name": "Main Distribution Center",
            "code": "MDC",
            "warehouse_type": "distribution",
            "address": "1000 Warehouse Drive",
            "city": "Memphis",
            "state": "TN",
            "postal_code": "38118",
            "country": "USA",
            "manager": admin_user
        },
        {
            "name": "West Coast Facility",
            "code": "WCF",
            "warehouse_type": "main",
            "address": "2500 Pacific Coast Hwy",
            "city": "Los Angeles",
            "state": "CA",
            "postal_code": "90404",
            "country": "USA",
            "manager": admin_user
        },
        {
            "name": "East Coast Hub",
            "code": "ECH",
            "warehouse_type": "distribution",
            "address": "500 Atlantic Avenue",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "USA",
            "manager": admin_user
        },
    ]
    
    warehouses = []
    for wh_data in warehouses_data:
        warehouse, created = Warehouse.objects.get_or_create(
            code=wh_data["code"],
            defaults=wh_data
        )
        warehouses.append(warehouse)
        if created:
            print(f"  ✅ Created warehouse: {warehouse.name}")
    
    # Create locations for each warehouse
    locations = []
    for warehouse in warehouses:
        # Create zones
        zones = ['A', 'B', 'C', 'D']
        for zone_code in zones:
            zone, created = Location.objects.get_or_create(
                warehouse=warehouse,
                code=zone_code,
                defaults={
                    "name": f"Zone {zone_code}",
                    "location_type": "zone",
                    "barcode": f"ZONE-{warehouse.code}-{zone_code}"
                }
            )
            locations.append(zone)
            if created:
                print(f"    ✅ Created zone: {zone.name} in {warehouse.name}")
            
            # Create aisles within zones
            for aisle_num in range(1, 4):  # 3 aisles per zone
                aisle_code = f"{zone_code}{aisle_num:02d}"
                aisle, created = Location.objects.get_or_create(
                    warehouse=warehouse,
                    code=aisle_code,
                    defaults={
                        "name": f"Aisle {aisle_code}",
                        "location_type": "aisle",
                        "parent": zone,
                        "barcode": f"AISLE-{warehouse.code}-{aisle_code}"
                    }
                )
                locations.append(aisle)
                if created:
                    print(f"      ✅ Created aisle: {aisle.name}")
                
                # Create racks within aisles
                for rack_num in range(1, 6):  # 5 racks per aisle
                    rack_code = f"{aisle_code}R{rack_num}"
                    rack, created = Location.objects.get_or_create(
                        warehouse=warehouse,
                        code=rack_code,
                        defaults={
                            "name": f"Rack {rack_code}",
                            "location_type": "rack",
                            "parent": aisle,
                            "barcode": f"RACK-{warehouse.code}-{rack_code}"
                        }
                    )
                    locations.append(rack)
                    if created:
                        print(f"        ✅ Created rack: {rack.name}")
    
    # Create bin locations
    bin_locations = []
    rack_locations = Location.objects.filter(location_type='rack')
    for rack in rack_locations[:20]:  # Create bins for first 20 racks
        for shelf in range(1, 5):  # 4 shelves per rack
            for bin_num in range(1, 4):  # 3 bins per shelf
                bin_code = f"S{shelf}B{bin_num}"
                bin_location, created = BinLocation.objects.get_or_create(
                    location=rack,
                    bin_code=bin_code,
                    defaults={
                        "barcode": f"BIN-{rack.warehouse.code}-{rack.code}-{bin_code}",
                        "capacity": Decimal(str(random.uniform(50, 200))),
                        "max_weight": Decimal(str(random.uniform(100, 500)))
                    }
                )
                bin_locations.append(bin_location)
                if created:
                    print(f"          ✅ Created bin: {bin_location.bin_code} in {rack.name}")
    
    return warehouses, locations, bin_locations

def create_product_templates_and_variants(categories, tags):
    """Create product templates with variants"""
    print("📋 Creating product templates and variants...")
    
    templates_data = [
        {
            "name": "Laptop Computer",
            "description": "High-performance business laptop",
            "category": "Computers",
            "brand": "TechCorp",
            "manufacturer": "TechCorp Manufacturing",
            "base_unit_of_measure": "pcs",
            "track_batches": False,
            "track_expiry": False,
            "track_serial": True,
            "tags": ["High Value", "Fragile", "Serialized"]
        },
        {
            "name": "Office Chair",
            "description": "Ergonomic office chair with adjustable height",
            "category": "Office Supplies",
            "brand": "ComfortSeating",
            "manufacturer": "Furniture Corp",
            "base_unit_of_measure": "pcs",
            "track_batches": True,
            "track_expiry": False,
            "track_serial": False,
            "tags": ["Bulk Only"]
        },
        {
            "name": "Industrial Drill Bit Set",
            "description": "Professional grade drill bit set",
            "category": "Power Tools",
            "brand": "ProTools",
            "manufacturer": "Industrial Tools Inc",
            "base_unit_of_measure": "pcs",
            "track_batches": True,
            "track_expiry": False,
            "track_serial": False,
            "tags": ["Fast Moving"]
        },
        {
            "name": "Chemical Solvent",
            "description": "Industrial cleaning solvent",
            "category": "Chemicals",
            "brand": "ChemClean",
            "manufacturer": "ChemTech Industries",
            "base_unit_of_measure": "liter",
            "track_batches": True,
            "track_expiry": True,
            "track_serial": False,
            "tags": ["Hazardous", "Expirable", "Temperature Controlled"]
        },
    ]
    
    templates = []
    variants = []
    
    for template_data in templates_data:
        # Get category
        category = Category.objects.filter(name=template_data["category"]).first()
        
        # Create template
        template, created = ProductTemplate.objects.get_or_create(
            name=template_data["name"],
            defaults={
                "description": template_data["description"],
                "category": category,
                "brand": template_data["brand"],
                "manufacturer": template_data["manufacturer"],
                "base_unit_of_measure": template_data["base_unit_of_measure"],
                "track_batches": template_data["track_batches"],
                "track_expiry": template_data["track_expiry"],
                "track_serial": template_data["track_serial"],
            }
        )
        
        if created:
            # Add tags
            template_tags = Tag.objects.filter(name__in=template_data["tags"])
            template.tags.set(template_tags)
            print(f"  ✅ Created template: {template.name}")
        
        templates.append(template)
        
        # Create variants for each template
        if template.name == "Laptop Computer":
            laptop_variants = [
                {"name": "Laptop 15\" Intel i5 8GB", "variant_code": "15-I5-8", "size": "15 inch", "color": "Black", "cost_price": "800.00", "selling_price": "1200.00"},
                {"name": "Laptop 15\" Intel i7 16GB", "variant_code": "15-I7-16", "size": "15 inch", "color": "Silver", "cost_price": "1200.00", "selling_price": "1800.00"},
                {"name": "Laptop 13\" Intel i5 8GB", "variant_code": "13-I5-8", "size": "13 inch", "color": "Black", "cost_price": "700.00", "selling_price": "1100.00"},
            ]
            for variant_data in laptop_variants:
                variant, created = ProductVariant.objects.get_or_create(
                    template=template,
                    variant_code=variant_data["variant_code"],
                    defaults=variant_data
                )
                variants.append(variant)
                if created:
                    print(f"    ✅ Created variant: {variant.name}")
        
        elif template.name == "Office Chair":
            chair_variants = [
                {"name": "Office Chair - Black Leather", "variant_code": "BLK-LEATH", "color": "Black", "material": "Leather", "cost_price": "150.00", "selling_price": "250.00"},
                {"name": "Office Chair - Brown Fabric", "variant_code": "BRN-FABR", "color": "Brown", "material": "Fabric", "cost_price": "120.00", "selling_price": "200.00"},
                {"name": "Office Chair - Gray Mesh", "variant_code": "GRY-MESH", "color": "Gray", "material": "Mesh", "cost_price": "100.00", "selling_price": "180.00"},
            ]
            for variant_data in chair_variants:
                variant, created = ProductVariant.objects.get_or_create(
                    template=template,
                    variant_code=variant_data["variant_code"],
                    defaults=variant_data
                )
                variants.append(variant)
                if created:
                    print(f"    ✅ Created variant: {variant.name}")
        
        elif template.name == "Industrial Drill Bit Set":
            drill_variants = [
                {"name": "Drill Bit Set - HSS 10pc", "variant_code": "HSS-10", "size": "10 piece", "material": "HSS", "cost_price": "25.00", "selling_price": "45.00"},
                {"name": "Drill Bit Set - Carbide 15pc", "variant_code": "CARB-15", "size": "15 piece", "material": "Carbide", "cost_price": "45.00", "selling_price": "80.00"},
                {"name": "Drill Bit Set - Titanium 20pc", "variant_code": "TIT-20", "size": "20 piece", "material": "Titanium", "cost_price": "65.00", "selling_price": "120.00"},
            ]
            for variant_data in drill_variants:
                variant, created = ProductVariant.objects.get_or_create(
                    template=template,
                    variant_code=variant_data["variant_code"],
                    defaults=variant_data
                )
                variants.append(variant)
                if created:
                    print(f"    ✅ Created variant: {variant.name}")
        
        elif template.name == "Chemical Solvent":
            solvent_variants = [
                {"name": "Solvent Type A - 5L", "variant_code": "TYPE-A-5L", "size": "5 Liter", "cost_price": "15.00", "selling_price": "25.00"},
                {"name": "Solvent Type A - 20L", "variant_code": "TYPE-A-20L", "size": "20 Liter", "cost_price": "50.00", "selling_price": "85.00"},
                {"name": "Solvent Type B - 5L", "variant_code": "TYPE-B-5L", "size": "5 Liter", "cost_price": "20.00", "selling_price": "35.00"},
            ]
            for variant_data in solvent_variants:
                variant, created = ProductVariant.objects.get_or_create(
                    template=template,
                    variant_code=variant_data["variant_code"],
                    defaults=variant_data
                )
                variants.append(variant)
                if created:
                    print(f"    ✅ Created variant: {variant.name}")
    
    return templates, variants

def create_items_and_barcodes(variants, categories, tags):
    """Create items from variants and standalone items"""
    print("📦 Creating items and barcodes...")
    
    items = []
    barcodes = []
    
    # Create items from variants
    for variant in variants:
        # Generate SKU
        template_code = ''.join([word[0] for word in variant.template.name.split()]).upper()
        sku = f"{template_code}-{variant.variant_code}-{random.randint(100, 999)}"
        
        item, created = Item.objects.get_or_create(
            sku=sku,
            defaults={
                "name": variant.name,
                "description": f"{variant.template.description} - {variant.name}",
                "product_variant": variant,
                "unit_of_measure": variant.template.base_unit_of_measure,
                "cost_price": variant.cost_price,
                "selling_price": variant.selling_price,
                "minimum_stock": random.randint(5, 20),
                "reorder_point": random.randint(10, 30),
                "track_batches": variant.template.track_batches,
                "track_expiry": variant.template.track_expiry,
                "track_serial": variant.template.track_serial,
            }
        )
        items.append(item)
        if created:
            print(f"  ✅ Created item: {item.sku} - {item.name}")
            
            # Create barcode for item
            barcode_data = f"{random.randint(1000000000000, 9999999999999)}"  # 13-digit EAN
            barcode, barcode_created = Barcode.objects.get_or_create(
                item=item,
                barcode_data=barcode_data,
                defaults={
                    "barcode_type": "ean13",
                    "is_primary": True
                }
            )
            barcodes.append(barcode)
            if barcode_created:
                print(f"    ✅ Created barcode: {barcode.barcode_data}")
    
    # Create some standalone items (not from variants)
    standalone_items_data = [
        {
            "sku": "MISC-001",
            "name": "Miscellaneous Hardware",
            "description": "Various small hardware items",
            "category": "Industrial Equipment",
            "unit_of_measure": "pcs",
            "cost_price": "5.00",
            "selling_price": "12.00",
            "minimum_stock": 50,
            "reorder_point": 100,
            "tags": ["Fast Moving"]
        },
        {
            "sku": "PACK-001",
            "name": "Packaging Materials",
            "description": "Cardboard boxes and packaging supplies",
            "category": "Office Supplies",
            "unit_of_measure": "box",
            "cost_price": "2.50",
            "selling_price": "5.00",
            "minimum_stock": 100,
            "reorder_point": 200,
            "tags": ["Bulk Only"]
        },
    ]
    
    for item_data in standalone_items_data:
        category = Category.objects.filter(name=item_data["category"]).first()
        item_tags = Tag.objects.filter(name__in=item_data.get("tags", []))
        
        item, created = Item.objects.get_or_create(
            sku=item_data["sku"],
            defaults={
                "name": item_data["name"],
                "description": item_data["description"],
                "category": category,
                "unit_of_measure": item_data["unit_of_measure"],
                "cost_price": Decimal(item_data["cost_price"]),
                "selling_price": Decimal(item_data["selling_price"]),
                "minimum_stock": item_data["minimum_stock"],
                "reorder_point": item_data["reorder_point"],
            }
        )
        
        if created:
            item.tags.set(item_tags)
            items.append(item)
            print(f"  ✅ Created standalone item: {item.sku} - {item.name}")
            
            # Create barcode
            barcode_data = f"{random.randint(1000000000000, 9999999999999)}"
            barcode, barcode_created = Barcode.objects.get_or_create(
                item=item,
                barcode_data=barcode_data,
                defaults={
                    "barcode_type": "ean13",
                    "is_primary": True
                }
            )
            barcodes.append(barcode)
            if barcode_created:
                print(f"    ✅ Created barcode: {barcode.barcode_data}")
    
    return items, barcodes

def create_batches_and_stock(items, suppliers, warehouses, locations, bin_locations):
    """Create batches and stock levels"""
    print("📊 Creating batches and stock levels...")
    
    batches = []
    stock_levels = []
    stock_movements = []
    
    # Create batches for items that track batches
    batch_items = [item for item in items if item.track_batches]
    
    for item in batch_items:
        # Create 2-3 batches per item
        for batch_num in range(1, random.randint(2, 4)):
            batch_number = f"B{datetime.now().year}{batch_num:03d}{random.randint(10, 99)}"
            
            # Random dates
            manufactured_date = date.today() - timedelta(days=random.randint(30, 180))
            received_date = manufactured_date + timedelta(days=random.randint(1, 30))
            
            expiry_date = None
            if item.track_expiry:
                expiry_date = received_date + timedelta(days=random.randint(365, 1095))
            
            batch, created = Batch.objects.get_or_create(
                item=item,
                batch_number=batch_number,
                defaults={
                    "supplier": random.choice(suppliers),
                    "manufactured_date": manufactured_date,
                    "expiry_date": expiry_date,
                    "received_date": received_date,
                    "quality_status": random.choice(["approved", "approved", "approved", "pending"]),
                    "notes": f"Batch received from supplier on {received_date}"
                }
            )
            batches.append(batch)
            if created:
                print(f"  ✅ Created batch: {batch.batch_number} for {item.sku}")
    
    # Create stock levels for all items
    for item in items:
        # Each item will have stock in 1-3 locations
        num_locations = random.randint(1, 3)
        selected_bin_locations = random.sample(bin_locations, min(num_locations, len(bin_locations)))
        
        for bin_location in selected_bin_locations:
            # Determine if we need a batch
            batch = None
            if item.track_batches and batches:
                item_batches = [b for b in batches if b.item == item]
                if item_batches:
                    batch = random.choice(item_batches)
            
            quantity = random.randint(10, 500)
            reserved_quantity = random.randint(0, min(10, quantity // 2))
            
            stock_level, created = StockLevel.objects.get_or_create(
                item=item,
                warehouse=bin_location.location.warehouse,
                location=bin_location.location,
                bin_location=bin_location,
                batch=batch,
                defaults={
                    "quantity": quantity,
                    "reserved_quantity": reserved_quantity,
                    "last_counted": datetime.now() - timedelta(days=random.randint(1, 30))
                }
            )
            stock_levels.append(stock_level)
            if created:
                print(f"  ✅ Created stock level: {item.sku} - {quantity} units at {stock_level.full_location_path}")
                
                # Create initial stock movement (receipt)
                movement, movement_created = StockMovement.objects.get_or_create(
                    reference_number=f"REC-{random.randint(100000, 999999)}",
                    defaults={
                        "movement_type": "receipt",
                        "item": item,
                        "warehouse": bin_location.location.warehouse,
                        "location": bin_location.location,
                        "bin_location": bin_location,
                        "batch": batch,
                        "quantity": quantity,
                        "unit_cost": item.cost_price,
                        "reason": "Initial stock receipt",
                        "notes": f"Initial stock receipt for {item.name}",
                        "performed_by": User.objects.get(username='admin')
                    }
                )
                stock_movements.append(movement)
                if movement_created:
                    print(f"    ✅ Created stock movement: {movement.reference_number}")
    
    return batches, stock_levels, stock_movements

def create_labels():
    """Create label templates"""
    print("🏷️  Creating label templates...")
    
    labels_data = [
        {
            "name": "Standard Item Label",
            "label_type": "item",
            "template": "<div><strong>{{item.sku}}</strong><br>{{item.name}}<br>{{barcode}}</div>",
            "width": Decimal("4.00"),
            "height": Decimal("2.00"),
            "is_default": True
        },
        {
            "name": "Location Label",
            "label_type": "location",
            "template": "<div><strong>{{location.name}}</strong><br>{{location.code}}<br>{{barcode}}</div>",
            "width": Decimal("3.00"),
            "height": Decimal("1.50"),
            "is_default": True
        },
        {
            "name": "Bin Label",
            "label_type": "bin",
            "template": "<div><strong>{{bin.bin_code}}</strong><br>{{bin.location.name}}<br>{{barcode}}</div>",
            "width": Decimal("2.00"),
            "height": Decimal("1.00"),
            "is_default": True
        },
    ]
    
    labels = []
    for label_data in labels_data:
        label, created = Label.objects.get_or_create(
            name=label_data["name"],
            defaults=label_data
        )
        labels.append(label)
        if created:
            print(f"  ✅ Created label template: {label.name}")
    
    return labels

def create_reservations_and_cycle_counts(items, stock_levels):
    """Create stock reservations and cycle counts"""
    print("📋 Creating reservations and cycle counts...")
    
    reservations = []
    cycle_counts = []
    
    # Create some stock reservations
    for _ in range(10):
        stock_level = random.choice(stock_levels)
        if stock_level.available_quantity > 0:
            reservation_qty = random.randint(1, min(5, stock_level.available_quantity))
            
            reservation, created = StockReservation.objects.get_or_create(
                item=stock_level.item,
                warehouse=stock_level.warehouse,
                location=stock_level.location,
                bin_location=stock_level.bin_location,
                batch=stock_level.batch,
                quantity=reservation_qty,
                reference_number=f"ORD-{random.randint(100000, 999999)}",
                defaults={
                    "expires_at": datetime.now() + timedelta(days=random.randint(7, 30)),
                    "notes": f"Reserved for order processing",
                    "created_by": User.objects.get(username='admin')
                }
            )
            reservations.append(reservation)
            if created:
                print(f"  ✅ Created reservation: {reservation.reference_number} - {reservation_qty} units")
    
    # Create cycle counts
    warehouses = list(set(sl.warehouse for sl in stock_levels))
    for warehouse in warehouses[:2]:  # Create cycle counts for first 2 warehouses
        locations = list(set(sl.location for sl in stock_levels if sl.warehouse == warehouse))
        
        for location in locations[:3]:  # First 3 locations per warehouse
            cycle_count, created = CycleCount.objects.get_or_create(
                warehouse=warehouse,
                location=location,
                scheduled_date=date.today() + timedelta(days=random.randint(1, 30)),
                defaults={
                    "status": random.choice(["scheduled", "in_progress", "completed"]),
                    "assigned_to": User.objects.get(username='admin'),
                    "total_items": random.randint(10, 50),
                    "items_counted": random.randint(5, 25),
                    "discrepancies_found": random.randint(0, 3),
                    "notes": f"Scheduled cycle count for {location.name}"
                }
            )
            cycle_counts.append(cycle_count)
            if created:
                print(f"  ✅ Created cycle count: {cycle_count.count_id} for {warehouse.name}/{location.name}")
    
    return reservations, cycle_counts

def main():
    """Main function to generate all dummy data"""
    print("🚀 Starting Dummy Data Generation for Inventory Management System")
    print("=" * 70)
    
    try:
        # Create data in order of dependencies
        categories = create_categories()
        tags = create_tags()
        suppliers = create_suppliers()
        warehouses, locations, bin_locations = create_warehouses_and_locations()
        templates, variants = create_product_templates_and_variants(categories, tags)
        items, barcodes = create_items_and_barcodes(variants, categories, tags)
        batches, stock_levels, stock_movements = create_batches_and_stock(
            items, suppliers, warehouses, locations, bin_locations
        )
        labels = create_labels()
        reservations, cycle_counts = create_reservations_and_cycle_counts(items, stock_levels)
        
        print("\n🎉 Dummy data generation completed successfully!")
        print("\n📊 Summary:")
        print(f"  • Categories: {len(categories)}")
        print(f"  • Tags: {len(tags)}")
        print(f"  • Suppliers: {len(suppliers)}")
        print(f"  • Warehouses: {len(warehouses)}")
        print(f"  • Locations: {len(locations)}")
        print(f"  • Bin Locations: {len(bin_locations)}")
        print(f"  • Product Templates: {len(templates)}")
        print(f"  • Product Variants: {len(variants)}")
        print(f"  • Items: {len(items)}")
        print(f"  • Barcodes: {len(barcodes)}")
        print(f"  • Batches: {len(batches)}")
        print(f"  • Stock Levels: {len(stock_levels)}")
        print(f"  • Stock Movements: {len(stock_movements)}")
        print(f"  • Labels: {len(labels)}")
        print(f"  • Reservations: {len(reservations)}")
        print(f"  • Cycle Counts: {len(cycle_counts)}")
        
        print("\n🌐 Access your application:")
        print("  • Frontend: http://localhost:3000")
        print("  • Backend API: http://localhost:8000/api")
        print("  • API Documentation: http://localhost:8000/api/docs/")
        print("  • Django Admin: http://localhost:8000/admin")
        print("    Username: admin")
        print("    Password: admin123")
        
    except Exception as e:
        print(f"\n❌ Error generating dummy data: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)