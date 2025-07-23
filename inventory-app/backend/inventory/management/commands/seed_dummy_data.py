from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from inventory.models import (
    Category,
    Tag,
    Supplier,
    Warehouse,
    Location,
    BinLocation,
    ProductTemplate,
    ProductVariant,
    Item,
    Barcode,
    StockLevel,
)

from faker import Faker
from decimal import Decimal
import random


class Command(BaseCommand):
    """Seed the database with dummy data for development / testing"""

    help = "Populate the database with realistic looking dummy data. " \
           "Intended for local development and testing environments."

    def add_arguments(self, parser):
        parser.add_argument(
            "--items",
            type=int,
            default=50,
            help="Number of inventory items (and related records) to create",
        )
        parser.add_argument(
            "--with-superuser",
            action="store_true",
            help="Create a default superuser (username: admin / password: admin)",
        )

    def handle(self, *args, **options):
        faker = Faker()

        # -- Optional superuser -------------------------------------------------
        if options["with_superuser"]:
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password="admin",
                )
                self.stdout.write(self.style.SUCCESS("Superuser 'admin' created (password: admin)"))
            else:
                self.stdout.write("Superuser 'admin' already exists – skipping")

        # ---------------------------------------------------------------------
        # Lookup or create core reference data so we can safely re-run command.
        # ---------------------------------------------------------------------
        category_count = 5
        tag_count = 8
        supplier_count = 5

        for _ in range(category_count):
            Category.objects.get_or_create(
                name=faker.unique.word().capitalize(),
                defaults={"description": faker.sentence()},
            )

        for _ in range(tag_count):
            Tag.objects.get_or_create(
                name=faker.unique.word(),
                defaults={"color": faker.hex_color()},
            )

        for _ in range(supplier_count):
            Supplier.objects.get_or_create(
                name=faker.company(),
                defaults={
                    "contact_person": faker.name(),
                    "email": faker.company_email(),
                    "phone": faker.phone_number(),
                    "address": faker.address(),
                },
            )

        warehouse, _ = Warehouse.objects.get_or_create(
            code="WH001",
            defaults={
                "name": "Main Warehouse",
                "warehouse_type": "main",
                "address": faker.address(),
            },
        )

        zone, _ = Location.objects.get_or_create(
            warehouse=warehouse,
            code="Z01",
            defaults={
                "name": "Zone 01",
                "location_type": "zone",
            },
        )

        bin_loc, _ = BinLocation.objects.get_or_create(
            location=zone,
            bin_code="B01",
        )

        # ---------------------------------------------------------------------
        # Product templates and variants
        # ---------------------------------------------------------------------
        templates_to_create = max(10, options["items"] // 5)
        categories = list(Category.objects.all())
        tags = list(Tag.objects.all())

        created_variants = []
        for _ in range(templates_to_create):
            template_name = f"{faker.color_name()} {faker.word().capitalize()}"
            template = ProductTemplate.objects.create(
                name=template_name,
                description=faker.sentence(),
                category=random.choice(categories) if categories else None,
                brand=faker.company(),
                base_unit_of_measure="pcs",
            )

            # Randomly attach 0-3 tags
            if tags:
                template.tags.set(random.sample(tags, k=random.randint(0, min(3, len(tags)))))

            # Create 2 variants per template
            for v in range(1, 3):
                variant = ProductVariant.objects.create(
                    template=template,
                    name=f"{template_name} Variant {v}",
                    variant_code=f"{template.id:03d}-V{v}",
                    size=random.choice(["S", "M", "L", "XL"]),
                    color=faker.safe_color_name(),
                    cost_price=Decimal(f"{random.uniform(5, 30):.2f}"),
                    selling_price=Decimal(f"{random.uniform(31, 60):.2f}"),
                )
                created_variants.append(variant)

        # ---------------------------------------------------------------------
        # Items, barcodes and stock levels
        # ---------------------------------------------------------------------
        unit_choices = [choice[0] for choice in Item.UNIT_CHOICES]
        items_to_create = options["items"]

        for i in range(items_to_create):
            variant = random.choice(created_variants)
            sku = f"SKU{variant.id:04d}-{i:03d}"

            item = Item.objects.create(
                sku=sku,
                name=f"{variant.name} Item",
                product_variant=variant,
                unit_of_measure=random.choice(unit_choices),
                minimum_stock=10,
                reorder_point=5,
            )

            # Primary barcode
            Barcode.objects.create(
                item=item,
                barcode_type="ean13",
                barcode_data=faker.unique.ean(length=13),
                is_primary=True,
            )

            # Stock level
            StockLevel.objects.create(
                item=item,
                warehouse=warehouse,
                location=zone,
                bin_location=bin_loc,
                quantity=random.randint(20, 100),
            )

        self.stdout.write(self.style.SUCCESS("✅  Dummy data generation complete!"))