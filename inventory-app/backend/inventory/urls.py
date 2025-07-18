from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, SupplierViewSet, LocationViewSet, ItemViewSet,
    BatchViewSet, StockLevelViewSet, StockMovementViewSet,
    StockReservationViewSet, CycleCountViewSet, CycleCountItemViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'items', ItemViewSet)
router.register(r'batches', BatchViewSet)
router.register(r'stock-levels', StockLevelViewSet)
router.register(r'stock-movements', StockMovementViewSet)
router.register(r'stock-reservations', StockReservationViewSet)
router.register(r'cycle-counts', CycleCountViewSet)
router.register(r'cycle-count-items', CycleCountItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]