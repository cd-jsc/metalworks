from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    Category, Tag, Supplier, Warehouse, Location, BinLocation, 
    ProductTemplate, ProductVariant, Item, Barcode, Label, Batch, 
    StockLevel, StockMovement, StockReservation, CycleCount, CycleCountItem
)
from .serializers import (
    CategorySerializer, TagSerializer, SupplierSerializer, WarehouseSerializer,
    LocationSerializer, BinLocationSerializer, ProductTemplateSerializer, 
    ProductVariantSerializer, ItemSerializer, BarcodeSerializer, LabelSerializer,
    BatchSerializer, StockLevelSerializer, StockMovementSerializer,
    StockReservationSerializer, CycleCountSerializer, CycleCountItemSerializer,
    CategorySelectSerializer, TagSelectSerializer, SupplierSelectSerializer,
    WarehouseSelectSerializer, LocationSelectSerializer, BinLocationSelectSerializer,
    ProductTemplateSelectSerializer, ProductVariantSelectSerializer, ItemSelectSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def select_options(self, request):
        """Get simplified category list for dropdowns"""
        categories = Category.objects.all()
        serializer = CategorySelectSerializer(categories, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def select_options(self, request):
        """Get simplified tag list for dropdowns"""
        tags = Tag.objects.all()
        serializer = TagSelectSerializer(tags, many=True)
        return Response(serializer.data)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'contact_person', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def select_options(self, request):
        """Get simplified supplier list for dropdowns"""
        suppliers = Supplier.objects.filter(is_active=True)
        serializer = SupplierSelectSerializer(suppliers, many=True)
        return Response(serializer.data)


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['warehouse_type', 'is_active']
    search_fields = ['name', 'code', 'address', 'city']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def select_options(self, request):
        """Get simplified warehouse list for dropdowns"""
        warehouses = Warehouse.objects.filter(is_active=True)
        serializer = WarehouseSelectSerializer(warehouses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stock_summary(self, request, pk=None):
        """Get stock summary for a specific warehouse"""
        warehouse = self.get_object()
        stock_levels = StockLevel.objects.filter(warehouse=warehouse).select_related('item')
        
        summary = {
            'warehouse': warehouse.name,
            'total_items': stock_levels.count(),
            'total_quantity': sum(stock.quantity for stock in stock_levels),
            'low_stock_items': sum(1 for stock in stock_levels if stock.item.is_low_stock),
            'locations': StockLevel.objects.filter(warehouse=warehouse).values('location__name').annotate(
                total_qty=Sum('quantity')
            )
        }
        return Response(summary)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['warehouse', 'location_type', 'parent', 'is_active']
    search_fields = ['name', 'code', 'barcode']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['warehouse__name', 'name']

    @action(detail=False, methods=['get'])
    def select_options(self, request):
        """Get simplified location list for dropdowns"""
        locations = Location.objects.filter(is_active=True).select_related('warehouse')
        serializer = LocationSelectSerializer(locations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stock_summary(self, request, pk=None):
        """Get stock summary for a specific location"""
        location = self.get_object()
        stock_levels = StockLevel.objects.filter(location=location).select_related('item')
        
        summary = {
            'location': location.name,
            'warehouse': location.warehouse.name,
            'total_items': stock_levels.count(),
            'total_quantity': sum(stock.quantity for stock in stock_levels),
            'low_stock_items': sum(1 for stock in stock_levels if stock.item.is_low_stock),
            'items': StockLevelSerializer(stock_levels, many=True).data
        }
        return Response(summary)


class BinLocationViewSet(viewsets.ModelViewSet):
    queryset = BinLocation.objects.all()
    serializer_class = BinLocationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'is_active']
    search_fields = ['bin_code', 'barcode']
    ordering_fields = ['bin_code', 'created_at']
    ordering = ['location__name', 'bin_code']

    @action(detail=False, methods=['get'])
    def select_options(self, request):
        """Get simplified bin location list for dropdowns"""
        bins = BinLocation.objects.filter(is_active=True).select_related('location')
        serializer = BinLocationSelectSerializer(bins, many=True)
        return Response(serializer.data)


class ProductTemplateViewSet(viewsets.ModelViewSet):
    queryset = ProductTemplate.objects.all()
    serializer_class = ProductTemplateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'brand', 'manufacturer', 'is_active']
    search_fields = ['name', 'description', 'brand', 'manufacturer']
    ordering_fields = ['name', 'brand', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related('tags', 'variants')

    @action(detail=False, methods=['get'])
    def select_options(self, request):
        """Get simplified product template list for dropdowns"""
        templates = ProductTemplate.objects.filter(is_active=True)
        serializer = ProductTemplateSelectSerializer(templates, many=True)
        return Response(serializer.data)


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['template', 'size', 'color', 'material', 'is_active']
    search_fields = ['name', 'variant_code', 'size', 'color', 'material', 'style']
    ordering_fields = ['name', 'variant_code', 'created_at']
    ordering = ['template__name', 'name']

    @action(detail=False, methods=['get'])
    def select_options(self, request):
        """Get simplified product variant list for dropdowns"""
        variants = ProductVariant.objects.filter(is_active=True).select_related('template')
        serializer = ProductVariantSelectSerializer(variants, many=True)
        return Response(serializer.data)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'product_variant', 'unit_of_measure', 'track_batches', 'track_expiry', 'is_active']
    search_fields = ['sku', 'name', 'description']
    ordering_fields = ['sku', 'name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'product_variant', 'created_by').prefetch_related('stock_levels', 'tags', 'barcodes')

    @action(detail=False, methods=['get'])
    def select_options(self, request):
        """Get simplified item list for dropdowns"""
        items = Item.objects.filter(is_active=True)
        serializer = ItemSelectSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get items with low stock levels"""
        items = Item.objects.filter(is_active=True)
        low_stock_items = [item for item in items if item.is_low_stock]
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stock_history(self, request, pk=None):
        """Get stock movement history for an item"""
        item = self.get_object()
        movements = StockMovement.objects.filter(item=item).order_by('-created_at')
        serializer = StockMovementSerializer(movements, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        """Adjust stock level for an item"""
        item = self.get_object()
        warehouse_id = request.data.get('warehouse')
        location_id = request.data.get('location')
        bin_location_id = request.data.get('bin_location')
        quantity = request.data.get('quantity')
        reason = request.data.get('reason', 'Manual adjustment')
        
        if not warehouse_id or not location_id or quantity is None:
            return Response({'error': 'Warehouse, location and quantity are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            warehouse = Warehouse.objects.get(id=warehouse_id)
            location = Location.objects.get(id=location_id)
            bin_location = None
            if bin_location_id:
                bin_location = BinLocation.objects.get(id=bin_location_id)
            
            # Create stock movement record
            movement = StockMovement.objects.create(
                movement_type='adjustment',
                reference_number=f'ADJ-{timezone.now().strftime("%Y%m%d%H%M%S")}',
                item=item,
                warehouse=warehouse,
                location=location,
                bin_location=bin_location,
                quantity=abs(quantity),
                reason=reason,
                performed_by=request.user
            )
            
            # Update or create stock level
            stock_level, created = StockLevel.objects.get_or_create(
                item=item,
                warehouse=warehouse,
                location=location,
                bin_location=bin_location,
                defaults={'quantity': 0}
            )
            
            stock_level.quantity = max(0, stock_level.quantity + quantity)
            stock_level.save()
            
            return Response({'message': 'Stock adjusted successfully'})
            
        except (Warehouse.DoesNotExist, Location.DoesNotExist, BinLocation.DoesNotExist):
            return Response({'error': 'Warehouse, location or bin location not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def generate_barcode(self, request, pk=None):
        """Generate a new barcode for an item"""
        item = self.get_object()
        barcode_type = request.data.get('barcode_type', 'ean13')
        
        # Generate barcode data (simplified - in production, use proper barcode generation)
        import random
        if barcode_type == 'ean13':
            barcode_data = ''.join([str(random.randint(0, 9)) for _ in range(13)])
        else:
            barcode_data = f"{item.sku}-{random.randint(1000, 9999)}"
        
        barcode = Barcode.objects.create(
            item=item,
            barcode_type=barcode_type,
            barcode_data=barcode_data,
            is_primary=not item.barcodes.exists()  # First barcode is primary
        )
        
        serializer = BarcodeSerializer(barcode)
        return Response(serializer.data)


class BarcodeViewSet(viewsets.ModelViewSet):
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['item', 'barcode_type', 'is_primary', 'is_active']
    search_fields = ['barcode_data', 'item__sku', 'item__name']
    ordering_fields = ['barcode_data', 'created_at']
    ordering = ['item__sku', '-is_primary']

    @action(detail=False, methods=['post'])
    def lookup_item(self, request):
        """Look up item by barcode"""
        barcode_data = request.data.get('barcode_data')
        if not barcode_data:
            return Response({'error': 'Barcode data is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            barcode = Barcode.objects.get(barcode_data=barcode_data, is_active=True)
            item_serializer = ItemSerializer(barcode.item)
            return Response({
                'item': item_serializer.data,
                'barcode': BarcodeSerializer(barcode).data
            })
        except Barcode.DoesNotExist:
            return Response({'error': 'Item not found for this barcode'}, 
                          status=status.HTTP_404_NOT_FOUND)


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['label_type', 'is_default', 'is_active']
    search_fields = ['name']
    ordering_fields = ['name', 'label_type', 'created_at']
    ordering = ['label_type', 'name']

    @action(detail=True, methods=['post'])
    def print_label(self, request, pk=None):
        """Print a label with provided data"""
        label = self.get_object()
        label_data = request.data.get('label_data', {})
        
        # In a real implementation, this would generate the label and send to printer
        # For now, we'll just return the label template with data
        return Response({
            'label': LabelSerializer(label).data,
            'rendered_template': f"Label printed with data: {label_data}",
            'status': 'success'
        })


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['item', 'supplier', 'quality_status']
    search_fields = ['batch_number', 'item__sku', 'item__name']
    ordering_fields = ['batch_number', 'expiry_date', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Get batches expiring within next 30 days"""
        thirty_days_from_now = timezone.now().date() + timedelta(days=30)
        batches = Batch.objects.filter(
            expiry_date__lte=thirty_days_from_now,
            expiry_date__gte=timezone.now().date()
        )
        serializer = self.get_serializer(batches, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expired(self, request):
        """Get expired batches"""
        batches = Batch.objects.filter(expiry_date__lt=timezone.now().date())
        serializer = self.get_serializer(batches, many=True)
        return Response(serializer.data)


class StockLevelViewSet(viewsets.ModelViewSet):
    queryset = StockLevel.objects.all()
    serializer_class = StockLevelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['item', 'warehouse', 'location', 'bin_location', 'batch']
    search_fields = ['item__sku', 'item__name', 'warehouse__name', 'location__name']
    ordering_fields = ['quantity', 'last_movement']
    ordering = ['item__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('item', 'warehouse', 'location', 'bin_location', 'batch')

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get stock level summary"""
        total_items = StockLevel.objects.count()
        total_quantity = StockLevel.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        zero_stock = StockLevel.objects.filter(quantity=0).count()
        
        return Response({
            'total_items': total_items,
            'total_quantity': total_quantity,
            'zero_stock_items': zero_stock,
            'warehouses': StockLevel.objects.values('warehouse__name').annotate(
                total_qty=Sum('quantity')
            ),
            'locations': StockLevel.objects.values('location__name').annotate(
                total_qty=Sum('quantity')
            )
        })


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['movement_type', 'item', 'warehouse', 'location', 'performed_by']
    search_fields = ['reference_number', 'item__sku', 'item__name', 'reason']
    ordering_fields = ['created_at', 'movement_type']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('item', 'warehouse', 'location', 'bin_location', 'batch', 'performed_by')

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent stock movements"""
        movements = StockMovement.objects.all()[:50]
        serializer = self.get_serializer(movements, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def transfer(self, request):
        """Transfer stock between locations"""
        item_id = request.data.get('item')
        from_warehouse_id = request.data.get('from_warehouse')
        from_location_id = request.data.get('from_location')
        from_bin_location_id = request.data.get('from_bin_location')
        to_warehouse_id = request.data.get('to_warehouse')
        to_location_id = request.data.get('to_location')
        to_bin_location_id = request.data.get('to_bin_location')
        quantity = request.data.get('quantity')
        reason = request.data.get('reason', 'Stock transfer')
        
        if not all([item_id, from_warehouse_id, from_location_id, to_warehouse_id, to_location_id, quantity]):
            return Response({'error': 'All required fields must be provided'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            item = Item.objects.get(id=item_id)
            from_warehouse = Warehouse.objects.get(id=from_warehouse_id)
            from_location = Location.objects.get(id=from_location_id)
            to_warehouse = Warehouse.objects.get(id=to_warehouse_id)
            to_location = Location.objects.get(id=to_location_id)
            
            from_bin_location = None
            to_bin_location = None
            if from_bin_location_id:
                from_bin_location = BinLocation.objects.get(id=from_bin_location_id)
            if to_bin_location_id:
                to_bin_location = BinLocation.objects.get(id=to_bin_location_id)
            
            # Check if enough stock available
            from_stock, _ = StockLevel.objects.get_or_create(
                item=item, 
                warehouse=from_warehouse, 
                location=from_location,
                bin_location=from_bin_location,
                defaults={'quantity': 0}
            )
            
            if from_stock.available_quantity < quantity:
                return Response({'error': 'Insufficient stock available'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Create transfer out movement
            ref_number = f'TRF-{timezone.now().strftime("%Y%m%d%H%M%S")}'
            StockMovement.objects.create(
                movement_type='transfer_out',
                reference_number=f'{ref_number}-OUT',
                item=item,
                warehouse=from_warehouse,
                location=from_location,
                bin_location=from_bin_location,
                quantity=quantity,
                to_warehouse=to_warehouse,
                to_location=to_location,
                to_bin_location=to_bin_location,
                reason=reason,
                performed_by=request.user
            )
            
            # Create transfer in movement
            StockMovement.objects.create(
                movement_type='transfer_in',
                reference_number=f'{ref_number}-IN',
                item=item,
                warehouse=to_warehouse,
                location=to_location,
                bin_location=to_bin_location,
                quantity=quantity,
                from_warehouse=from_warehouse,
                from_location=from_location,
                from_bin_location=from_bin_location,
                reason=reason,
                performed_by=request.user
            )
            
            # Update stock levels
            from_stock.quantity -= quantity
            from_stock.save()
            
            to_stock, _ = StockLevel.objects.get_or_create(
                item=item, 
                warehouse=to_warehouse, 
                location=to_location,
                bin_location=to_bin_location,
                defaults={'quantity': 0}
            )
            to_stock.quantity += quantity
            to_stock.save()
            
            return Response({'message': 'Transfer completed successfully'})
            
        except (Item.DoesNotExist, Warehouse.DoesNotExist, Location.DoesNotExist, BinLocation.DoesNotExist):
            return Response({'error': 'One or more entities not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StockReservationViewSet(viewsets.ModelViewSet):
    queryset = StockReservation.objects.all()
    serializer_class = StockReservationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['item', 'warehouse', 'location', 'is_active']
    search_fields = ['reference_number', 'item__sku', 'item__name']
    ordering_fields = ['reserved_at', 'expires_at']
    ordering = ['-reserved_at']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active reservations"""
        reservations = StockReservation.objects.filter(is_active=True)
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expiring(self, request):
        """Get reservations expiring soon"""
        tomorrow = timezone.now() + timedelta(days=1)
        reservations = StockReservation.objects.filter(
            is_active=True,
            expires_at__lte=tomorrow
        )
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)


class CycleCountViewSet(viewsets.ModelViewSet):
    queryset = CycleCount.objects.all()
    serializer_class = CycleCountSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['warehouse', 'location', 'status', 'assigned_to']
    search_fields = ['count_id', 'warehouse__name', 'location__name']
    ordering_fields = ['scheduled_date', 'created_at']
    ordering = ['-scheduled_date']

    @action(detail=True, methods=['post'])
    def start_count(self, request, pk=None):
        """Start a cycle count"""
        cycle_count = self.get_object()
        
        if cycle_count.status != 'scheduled':
            return Response({'error': 'Count is not in scheduled status'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        cycle_count.status = 'in_progress'
        cycle_count.actual_date = timezone.now().date()
        cycle_count.counted_by = request.user
        cycle_count.save()
        
        # Create cycle count items for all items in the warehouse/location
        if cycle_count.location:
            stock_levels = StockLevel.objects.filter(
                warehouse=cycle_count.warehouse,
                location=cycle_count.location
            )
        else:
            stock_levels = StockLevel.objects.filter(warehouse=cycle_count.warehouse)
        
        for stock in stock_levels:
            CycleCountItem.objects.create(
                cycle_count=cycle_count,
                item=stock.item,
                location=stock.location,
                bin_location=stock.bin_location,
                batch=stock.batch,
                system_quantity=stock.quantity
            )
        
        cycle_count.total_items = stock_levels.count()
        cycle_count.save()
        
        return Response({'message': 'Cycle count started successfully'})

    @action(detail=True, methods=['post'])
    def complete_count(self, request, pk=None):
        """Complete a cycle count"""
        cycle_count = self.get_object()
        
        if cycle_count.status != 'in_progress':
            return Response({'error': 'Count is not in progress'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate summary
        items = cycle_count.items.all()
        cycle_count.items_counted = items.filter(is_counted=True).count()
        cycle_count.discrepancies_found = items.filter(variance__ne=0).count()
        cycle_count.status = 'completed'
        cycle_count.save()
        
        return Response({'message': 'Cycle count completed successfully'})


class CycleCountItemViewSet(viewsets.ModelViewSet):
    queryset = CycleCountItem.objects.all()
    serializer_class = CycleCountItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cycle_count', 'item', 'location', 'is_counted']
    search_fields = ['item__sku', 'item__name']
    ordering_fields = ['counted_at']
    ordering = ['item__name']

    @action(detail=True, methods=['post'])
    def count_item(self, request, pk=None):
        """Record count for an item"""
        count_item = self.get_object()
        counted_quantity = request.data.get('counted_quantity')
        
        if counted_quantity is None:
            return Response({'error': 'Counted quantity is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        count_item.counted_quantity = counted_quantity
        count_item.is_counted = True
        count_item.counted_at = timezone.now()
        count_item.save()
        
        return Response({'message': 'Item counted successfully'})