from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .viewsets import (
    CategoryViewSet, ResponsibleForTestingViewSet, ResponsibleForQCViewSet,
    ProductPartViewSet, ProductCodeViewSet, QuarantineWarehouseViewSet,
    RawMaterialWarehouseViewSet, ProductWarehouseViewSet, ReturnedProductViewSet,
    ProductRawMaterialViewSet, SecondryWarehouseViewSet, SecondryWarehouseRawMaterialViewSet,
    ProductSecondryProductViewSet, ProductDeliveryViewSet, ProductDeliveryProductViewSet,
    ProductDeliverySecondryProductViewSet, ProductDeliveryRawMaterialViewSet,
    ExternalProductDeliveryViewSet, ExternalProductDeliveryProductViewSet,
    ExternalProductDeliverySecondryProductViewSet, ExternalProductDeliveryRawMaterialViewSet,
    ReturnedFromCustomerViewSet, BorrowedProductViewSet
)

# Create router
router = DefaultRouter()

# Register all ViewSets
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'responsible-testing', ResponsibleForTestingViewSet, basename='responsible-testing')
router.register(r'responsible-qc', ResponsibleForQCViewSet, basename='responsible-qc')
router.register(r'product-parts', ProductPartViewSet, basename='product-part')
router.register(r'product-codes', ProductCodeViewSet, basename='product-code')

# Warehouse related endpoints
router.register(r'quarantine-warehouse', QuarantineWarehouseViewSet, basename='quarantine-warehouse')
router.register(r'raw-material-warehouse', RawMaterialWarehouseViewSet, basename='raw-material-warehouse')
router.register(r'product-warehouse', ProductWarehouseViewSet, basename='product-warehouse')
router.register(r'secondry-warehouse', SecondryWarehouseViewSet, basename='secondry-warehouse')

# Returned products
router.register(r'returned-products', ReturnedProductViewSet, basename='returned-product')
router.register(r'returned-from-customer', ReturnedFromCustomerViewSet, basename='returned-from-customer')

# Product materials and relationships
router.register(r'product-raw-materials', ProductRawMaterialViewSet, basename='product-raw-material')
router.register(r'secondry-warehouse-raw-materials', SecondryWarehouseRawMaterialViewSet, basename='secondry-warehouse-raw-material')
router.register(r'product-secondry-products', ProductSecondryProductViewSet, basename='product-secondry-product')

# Delivery related endpoints
router.register(r'product-deliveries', ProductDeliveryViewSet, basename='product-delivery')
router.register(r'product-delivery-products', ProductDeliveryProductViewSet, basename='product-delivery-product')
router.register(r'product-delivery-secondry-products', ProductDeliverySecondryProductViewSet, basename='product-delivery-secondry-product')
router.register(r'product-delivery-raw-materials', ProductDeliveryRawMaterialViewSet, basename='product-delivery-raw-material')

# External delivery related endpoints
router.register(r'external-product-deliveries', ExternalProductDeliveryViewSet, basename='external-product-delivery')
router.register(r'external-product-delivery-products', ExternalProductDeliveryProductViewSet, basename='external-product-delivery-product')
router.register(r'external-product-delivery-secondry-products', ExternalProductDeliverySecondryProductViewSet, basename='external-product-delivery-secondry-product')
router.register(r'external-product-delivery-raw-materials', ExternalProductDeliveryRawMaterialViewSet, basename='external-product-delivery-raw-material')

# Borrowed products
router.register(r'borrowed-products', BorrowedProductViewSet, basename='borrowed-product')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', views.api_login_page, name='api_login'),
    path('api/login/submit/', views.APILoginView.as_view(), name='api_login_submit'),
    path('api/export/excel/', views.ExcelExportView.as_view(), name='export_all_excel'),
]
