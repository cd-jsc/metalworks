from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, TagViewSet, SupplierViewSet, WarehouseViewSet,
    LocationViewSet, BinLocationViewSet, ProductTemplateViewSet,
    ProductVariantViewSet, ItemViewSet, BarcodeViewSet, LabelViewSet,
    BatchViewSet, StockLevelViewSet, StockMovementViewSet,
    StockReservationViewSet, CycleCountViewSet, CycleCountItemViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'bin-locations', BinLocationViewSet)
router.register(r'product-templates', ProductTemplateViewSet)
router.register(r'product-variants', ProductVariantViewSet)
router.register(r'items', ItemViewSet)
router.register(r'barcodes', BarcodeViewSet)
router.register(r'labels', LabelViewSet)
router.register(r'batches', BatchViewSet)
router.register(r'stock-levels', StockLevelViewSet)
router.register(r'stock-movements', StockMovementViewSet)
router.register(r'stock-reservations', StockReservationViewSet)
router.register(r'cycle-counts', CycleCountViewSet)
router.register(r'cycle-count-items', CycleCountItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]