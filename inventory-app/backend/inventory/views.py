from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    Category, Supplier, Location, Item, Batch, StockLevel, 
    StockMovement, StockReservation, CycleCount, CycleCountItem
)
from .serializers import (
    CategorySerializer, SupplierSerializer, LocationSerializer, ItemSerializer,
    BatchSerializer, StockLevelSerializer, StockMovementSerializer,
    StockReservationSerializer, CycleCountSerializer, CycleCountItemSerializer,
    CategorySelectSerializer, SupplierSelectSerializer, LocationSelectSerializer,
    ItemSelectSerializer
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


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location_type', 'is_active']
    search_fields = ['name', 'code', 'address']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def select_options(self, request):
        """Get simplified location list for dropdowns"""
        locations = Location.objects.filter(is_active=True)
        serializer = LocationSelectSerializer(locations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stock_summary(self, request, pk=None):
        """Get stock summary for a specific location"""
        location = self.get_object()
        stock_levels = StockLevel.objects.filter(location=location).select_related('item')
        
        summary = {
            'location': location.name,
            'total_items': stock_levels.count(),
            'total_quantity': sum(stock.quantity for stock in stock_levels),
            'low_stock_items': sum(1 for stock in stock_levels if stock.item.is_low_stock),
            'items': StockLevelSerializer(stock_levels, many=True).data
        }
        return Response(summary)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'unit_of_measure', 'track_batches', 'track_expiry', 'is_active']
    search_fields = ['sku', 'name', 'description']
    ordering_fields = ['sku', 'name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Add prefetch for related data
        return queryset.select_related('category', 'created_by').prefetch_related('stock_levels')

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
        location_id = request.data.get('location')
        quantity = request.data.get('quantity')
        reason = request.data.get('reason', 'Manual adjustment')
        
        if not location_id or quantity is None:
            return Response({'error': 'Location and quantity are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            location = Location.objects.get(id=location_id)
            
            # Create stock movement record
            movement = StockMovement.objects.create(
                movement_type='adjustment',
                reference_number=f'ADJ-{timezone.now().strftime("%Y%m%d%H%M%S")}',
                item=item,
                location=location,
                quantity=abs(quantity),
                reason=reason,
                performed_by=request.user
            )
            
            # Update or create stock level
            stock_level, created = StockLevel.objects.get_or_create(
                item=item,
                location=location,
                defaults={'quantity': 0}
            )
            
            stock_level.quantity = max(0, stock_level.quantity + quantity)
            stock_level.save()
            
            return Response({'message': 'Stock adjusted successfully'})
            
        except Location.DoesNotExist:
            return Response({'error': 'Location not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    filterset_fields = ['item', 'location', 'batch']
    search_fields = ['item__sku', 'item__name', 'location__name']
    ordering_fields = ['quantity', 'last_movement']
    ordering = ['item__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('item', 'location', 'batch')

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
            'locations': StockLevel.objects.values('location__name').annotate(
                total_qty=Sum('quantity')
            )
        })


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['movement_type', 'item', 'location', 'performed_by']
    search_fields = ['reference_number', 'item__sku', 'item__name', 'reason']
    ordering_fields = ['created_at', 'movement_type']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('item', 'location', 'batch', 'performed_by')

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
        from_location_id = request.data.get('from_location')
        to_location_id = request.data.get('to_location')
        quantity = request.data.get('quantity')
        reason = request.data.get('reason', 'Stock transfer')
        
        if not all([item_id, from_location_id, to_location_id, quantity]):
            return Response({'error': 'All fields are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            item = Item.objects.get(id=item_id)
            from_location = Location.objects.get(id=from_location_id)
            to_location = Location.objects.get(id=to_location_id)
            
            # Check if enough stock available
            from_stock, _ = StockLevel.objects.get_or_create(
                item=item, location=from_location, defaults={'quantity': 0}
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
                location=from_location,
                quantity=quantity,
                to_location=to_location,
                reason=reason,
                performed_by=request.user
            )
            
            # Create transfer in movement
            StockMovement.objects.create(
                movement_type='transfer_in',
                reference_number=f'{ref_number}-IN',
                item=item,
                location=to_location,
                quantity=quantity,
                from_location=from_location,
                reason=reason,
                performed_by=request.user
            )
            
            # Update stock levels
            from_stock.quantity -= quantity
            from_stock.save()
            
            to_stock, _ = StockLevel.objects.get_or_create(
                item=item, location=to_location, defaults={'quantity': 0}
            )
            to_stock.quantity += quantity
            to_stock.save()
            
            return Response({'message': 'Transfer completed successfully'})
            
        except (Item.DoesNotExist, Location.DoesNotExist):
            return Response({'error': 'Item or location not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StockReservationViewSet(viewsets.ModelViewSet):
    queryset = StockReservation.objects.all()
    serializer_class = StockReservationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['item', 'location', 'is_active']
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
    filterset_fields = ['location', 'status', 'assigned_to']
    search_fields = ['count_id', 'location__name']
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
        
        # Create cycle count items for all items in the location
        stock_levels = StockLevel.objects.filter(location=cycle_count.location)
        for stock in stock_levels:
            CycleCountItem.objects.create(
                cycle_count=cycle_count,
                item=stock.item,
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
    filterset_fields = ['cycle_count', 'item', 'is_counted']
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