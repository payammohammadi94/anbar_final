from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth.models import User

from .models import (
    Category, ResponsibleForTesting, ResponsibleForQC, ProductPart, ProductCode,
    QuarantineWarehouse, RawMaterialWarehouse, ProductWarehouse, ReturnedProduct,
    ProductRawMaterial, SecondryWarehouse, SecondryWarehouseRawMaterial,
    ProductSecondryProduct, ProductDelivery, ProductDeliveryProduct,
    ProductDeliverySecondryProduct, ProductDeliveryRawMaterial,
    ExternalProductDelivery, ExternalProductDeliveryProduct,
    ExternalProductDeliverySecondryProduct, ExternalProductDeliveryRawMaterial,
    ReturnedFromCustomer, BorrowedProduct
)

from .serializers_optimized import (
    CategorySerializer, CategoryDetailSerializer, ResponsibleForTestingSerializer, 
    ResponsibleForQCSerializer, ProductPartSerializer, ProductCodeSerializer, 
    QuarantineWarehouseSerializer, RawMaterialWarehouseSerializer, 
    ProductWarehouseSerializer, ProductWarehouseDetailSerializer, 
    ReturnedProductSerializer, ProductRawMaterialSerializer, 
    SecondryWarehouseSerializer, SecondryWarehouseRawMaterialSerializer,
    ProductSecondryProductSerializer, ProductDeliverySerializer, 
    ProductDeliveryDetailSerializer, ProductDeliveryProductSerializer,
    ProductDeliverySecondryProductSerializer, ProductDeliveryRawMaterialSerializer,
    ExternalProductDeliverySerializer, ExternalProductDeliveryProductSerializer,
    ExternalProductDeliverySecondryProductSerializer, ExternalProductDeliveryRawMaterialSerializer,
    ReturnedFromCustomerSerializer, BorrowedProductSerializer
)
from .excel_export import WarehouseExcelExporter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_sub', 'sub_cat']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'id']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer

    @action(detail=True, methods=['get'])
    def sub_categories(self, request, pk=None):
        """دریافت زیر دسته‌های یک دسته"""
        category = self.get_object()
        sub_categories = category.catgory.all()
        serializer = CategorySerializer(sub_categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def main_categories(self, request):
        """دریافت دسته‌های اصلی (غیر زیر دسته)"""
        main_categories = Category.objects.filter(is_sub=False)
        serializer = CategorySerializer(main_categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export دسته‌بندی‌ها به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_categories(queryset)


class ResponsibleForTestingViewSet(viewsets.ModelViewSet):
    queryset = ResponsibleForTesting.objects.all()
    serializer_class = ResponsibleForTestingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_last_name']
    ordering_fields = ['first_last_name', 'id']
    ordering = ['first_last_name']

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export مسئولان تست به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_to_excel(queryset, 'responsible_for_testing')


class ResponsibleForQCViewSet(viewsets.ModelViewSet):
    queryset = ResponsibleForQC.objects.all()
    serializer_class = ResponsibleForQCSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_last_name']
    ordering_fields = ['first_last_name', 'id']
    ordering = ['first_last_name']

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export مسئولان QC به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_to_excel(queryset, 'responsible_for_qc')


class ProductPartViewSet(viewsets.ModelViewSet):
    queryset = ProductPart.objects.all()
    serializer_class = ProductPartSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_part']
    ordering_fields = ['product_part', 'id']
    ordering = ['product_part']

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export قطعات محصول به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_product_parts(queryset)


class ProductCodeViewSet(viewsets.ModelViewSet):
    queryset = ProductCode.objects.all()
    serializer_class = ProductCodeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_code']
    ordering_fields = ['product_code', 'id']
    ordering = ['product_code']

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export کدهای محصول به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_product_codes(queryset)


class QuarantineWarehouseViewSet(viewsets.ModelViewSet):
    queryset = QuarantineWarehouse.objects.select_related(
        'created_by', 'part_number', 'item_code', 'qc_responsible', 'test_responsible'
    ).prefetch_related('category').all()
    serializer_class = QuarantineWarehouseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'unit', 'destination', 'created_by']
    search_fields = ['piece_name', 'supplier', 'serial_number', 'item_code__product_code', 'part_number__product_part']
    ordering_fields = ['entry_date', 'piece_name', 'quantity', 'unit_price', 'id']
    ordering = ['-entry_date']

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """دریافت آیتم‌ها بر اساس وضعیت"""
        status_param = request.query_params.get('status')
        if status_param:
            items = self.queryset.filter(status=status_param)
            serializer = self.get_serializer(items, many=True)
            return Response(serializer.data)
        return Response({'error': 'وضعیت مورد نظر را مشخص کنید'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """آمار کلی انبار قرنطینه"""
        total_items = self.queryset.count()
        status_counts = {}
        for status_choice in QuarantineWarehouse.STATUS_CHOICES:
            status_counts[status_choice[0]] = self.queryset.filter(status=status_choice[0]).count()
        
        return Response({
            'total_items': total_items,
            'status_counts': status_counts
        })

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export انبار قرنطینه به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_quarantine_warehouse(queryset)


class RawMaterialWarehouseViewSet(viewsets.ModelViewSet):
    queryset = RawMaterialWarehouse.objects.select_related(
        'created_by', 'quarantine_reference', 'part_number', 'item_code'
    ).prefetch_related('category').all()
    serializer_class = RawMaterialWarehouseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['unit', 'created_by']
    search_fields = ['piece_name', 'serial_number', 'item_code__product_code', 'part_number__product_part']
    ordering_fields = ['entry_date', 'piece_name', 'quantity', 'price', 'id']
    ordering = ['-entry_date']

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """دریافت آیتم‌هایی که موجودی کمی دارند"""
        threshold = request.query_params.get('threshold', 10)
        try:
            threshold = int(threshold)
            low_stock_items = self.queryset.filter(quantity__lte=threshold)
            serializer = self.get_serializer(low_stock_items, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({'error': 'آستانه باید عدد باشد'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """آمار کلی انبار مواد اولیه"""
        total_items = self.queryset.count()
        total_quantity = sum(item.quantity for item in self.queryset)
        unit_counts = {}
        for unit_choice in RawMaterialWarehouse.UNIT_PRICE_CHOICES:
            unit_counts[unit_choice[0]] = self.queryset.filter(unit=unit_choice[0]).count()
        
        return Response({
            'total_items': total_items,
            'total_quantity': total_quantity,
            'unit_counts': unit_counts
        })

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export انبار مواد اولیه به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_raw_material_warehouse(queryset)


class ProductWarehouseViewSet(viewsets.ModelViewSet):
    queryset = ProductWarehouse.objects.select_related('created_by').prefetch_related(
        'raw_materials', 'secondry_products'
    ).all()
    serializer_class = ProductWarehouseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['created_by']
    search_fields = ['product_name', 'product_serial_number', 'deliverer', 'receiver']
    ordering_fields = ['manufacturing_start_date', 'product_name', 'id']
    ordering = ['-manufacturing_start_date']

    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        """محصولات در حال ساخت"""
        in_progress_products = self.queryset.filter(
            manufacturing_end_date__isnull=True
        )
        serializer = self.get_serializer(in_progress_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """محصولات تکمیل شده"""
        completed_products = self.queryset.filter(
            manufacturing_end_date__isnull=False
        )
        serializer = self.get_serializer(completed_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def raw_materials(self, request, pk=None):
        """مواد اولیه استفاده شده در محصول"""
        product = self.get_object()
        raw_materials = product.raw_materials.all()
        serializer = ProductRawMaterialSerializer(raw_materials, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def secondry_products(self, request, pk=None):
        """محصولات ثانویه استفاده شده در محصول"""
        product = self.get_object()
        secondry_products = product.secondry_products.all()
        serializer = ProductSecondryProductSerializer(secondry_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export انبار محصولات به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_product_warehouse(queryset)


class ReturnedProductViewSet(viewsets.ModelViewSet):
    queryset = ReturnedProduct.objects.select_related(
        'created_by', 'part_number', 'item_code'
    ).all()
    serializer_class = ReturnedProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['unit', 'created_by']
    search_fields = ['piece_name', 'supplier', 'serial_number', 'item_code__product_code', 'part_number__product_part']
    ordering_fields = ['return_date', 'piece_name', 'id']
    ordering = ['-return_date']

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export محصولات برگشتی به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_returned_products(queryset)


class ProductRawMaterialViewSet(viewsets.ModelViewSet):
    queryset = ProductRawMaterial.objects.select_related(
        'created_by', 'product', 'raw_material_source', 'part_number', 'item_code'
    ).all()
    serializer_class = ProductRawMaterialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'unit', 'created_by']
    search_fields = ['raw_material_name', 'user_who_used', 'serial_number', 'item_code__product_code', 'part_number__product_part']
    ordering_fields = ['raw_material_entry_date', 'raw_material_name', 'quantity', 'id']
    ordering = ['-raw_material_entry_date']


class SecondryWarehouseViewSet(viewsets.ModelViewSet):
    queryset = SecondryWarehouse.objects.select_related('created_by').prefetch_related(
        'raw_materials'
    ).all()
    serializer_class = SecondryWarehouseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['created_by']
    search_fields = ['product_name', 'product_serial_number', 'deliverer', 'receiver']
    ordering_fields = ['manufacturing_start_date', 'product_name', 'id']
    ordering = ['-manufacturing_start_date']

    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        """محصولات ثانویه در حال ساخت"""
        in_progress_products = self.queryset.filter(
            manufacturing_end_date__isnull=True
        )
        serializer = self.get_serializer(in_progress_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def raw_materials(self, request, pk=None):
        """مواد اولیه استفاده شده در محصول ثانویه"""
        product = self.get_object()
        raw_materials = product.raw_materials.all()
        serializer = SecondryWarehouseRawMaterialSerializer(raw_materials, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export انبار ثانویه به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_secondry_warehouse(queryset)


class SecondryWarehouseRawMaterialViewSet(viewsets.ModelViewSet):
    queryset = SecondryWarehouseRawMaterial.objects.select_related(
        'created_by', 'secondryWarehouse', 'raw_material_source', 'part_number', 'item_code'
    ).all()
    serializer_class = SecondryWarehouseRawMaterialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['secondryWarehouse', 'unit', 'created_by']
    search_fields = ['raw_material_name', 'user_who_used', 'serial_number', 'item_code__product_code', 'part_number__product_part']
    ordering_fields = ['raw_material_entry_date', 'raw_material_name', 'quantity', 'id']
    ordering = ['-raw_material_entry_date']


class ProductSecondryProductViewSet(viewsets.ModelViewSet):
    queryset = ProductSecondryProduct.objects.select_related(
        'product', 'secondry_product'
    ).all()
    serializer_class = ProductSecondryProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'secondry_product']
    search_fields = ['product__product_name', 'secondry_product__product_name']
    ordering_fields = ['quantity', 'id']
    ordering = ['-id']


class ProductDeliveryViewSet(viewsets.ModelViewSet):
    queryset = ProductDelivery.objects.select_related('deliverer').prefetch_related(
        'product_items', 'secondry_items', 'raw_material_items'
    ).all()
    serializer_class = ProductDeliverySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['deliverer']
    search_fields = ['receiver_name', 'user_name']
    ordering_fields = ['delivery_date', 'receiver_name', 'id']
    ordering = ['-delivery_date']

    @action(detail=False, methods=['get'])
    def pending_return(self, request):
        """تحویل‌هایی که هنوز برگشت داده نشده‌اند"""
        pending_deliveries = self.queryset.filter(return_date__isnull=True)
        serializer = self.get_serializer(pending_deliveries, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """تمام آیتم‌های یک تحویل"""
        delivery = self.get_object()
        result = {
            'products': ProductDeliveryProductSerializer(delivery.product_items.all(), many=True).data,
            'secondry_products': ProductDeliverySecondryProductSerializer(delivery.secondry_items.all(), many=True).data,
            'raw_materials': ProductDeliveryRawMaterialSerializer(delivery.raw_material_items.all(), many=True).data,
        }
        return Response(result)

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export تحویل محصولات به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_product_delivery(queryset)


class ProductDeliveryProductViewSet(viewsets.ModelViewSet):
    queryset = ProductDeliveryProduct.objects.select_related(
        'delivery', 'product'
    ).all()
    serializer_class = ProductDeliveryProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['delivery', 'product']
    search_fields = ['product__product_name', 'product__product_serial_number']
    ordering_fields = ['delivery_date', 'quantity', 'id']
    ordering = ['-delivery_date']


class ProductDeliverySecondryProductViewSet(viewsets.ModelViewSet):
    queryset = ProductDeliverySecondryProduct.objects.select_related(
        'delivery', 'secondry_product'
    ).all()
    serializer_class = ProductDeliverySecondryProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['delivery', 'secondry_product']
    search_fields = ['secondry_product__product_name', 'secondry_product__product_serial_number']
    ordering_fields = ['delivery_date', 'quantity', 'id']
    ordering = ['-delivery_date']


class ProductDeliveryRawMaterialViewSet(viewsets.ModelViewSet):
    queryset = ProductDeliveryRawMaterial.objects.select_related(
        'delivery', 'raw_material', 'part_number', 'item_code'
    ).all()
    serializer_class = ProductDeliveryRawMaterialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['delivery', 'raw_material', 'unit']
    search_fields = ['raw_material_name', 'user_who_used', 'serial_number', 'item_code__product_code', 'part_number__product_part']
    ordering_fields = ['delivery_date', 'quantity', 'id']
    ordering = ['-delivery_date']


class ExternalProductDeliveryViewSet(viewsets.ModelViewSet):
    queryset = ExternalProductDelivery.objects.select_related('deliverer').prefetch_related(
        'product_items', 'secondry_items', 'raw_material_items'
    ).all()
    serializer_class = ExternalProductDeliverySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['deliverer', 'reference_letter']
    search_fields = ['receiver_name']
    ordering_fields = ['delivery_date', 'receiver_name', 'id']
    ordering = ['-delivery_date']

    @action(detail=False, methods=['get'])
    def pending_return(self, request):
        """تحویل‌های خارجی که هنوز برگشت داده نشده‌اند"""
        pending_deliveries = self.queryset.filter(return_date__isnull=True)
        serializer = self.get_serializer(pending_deliveries, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """تمام آیتم‌های یک تحویل خارجی"""
        delivery = self.get_object()
        result = {
            'products': ExternalProductDeliveryProductSerializer(delivery.product_items.all(), many=True).data,
            'secondry_products': ExternalProductDeliverySecondryProductSerializer(delivery.secondry_items.all(), many=True).data,
            'raw_materials': ExternalProductDeliveryRawMaterialSerializer(delivery.raw_material_items.all(), many=True).data,
        }
        return Response(result)

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export تحویل محصولات خارجی به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_external_product_delivery(queryset)


class ExternalProductDeliveryProductViewSet(viewsets.ModelViewSet):
    queryset = ExternalProductDeliveryProduct.objects.select_related(
        'delivery', 'product'
    ).all()
    serializer_class = ExternalProductDeliveryProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['delivery', 'product']
    search_fields = ['product__product_name', 'product__product_serial_number']
    ordering_fields = ['delivery_date', 'quantity', 'id']
    ordering = ['-delivery_date']


class ExternalProductDeliverySecondryProductViewSet(viewsets.ModelViewSet):
    queryset = ExternalProductDeliverySecondryProduct.objects.select_related(
        'delivery', 'secondry_product'
    ).all()
    serializer_class = ExternalProductDeliverySecondryProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['delivery', 'secondry_product']
    search_fields = ['secondry_product__product_name', 'secondry_product__product_serial_number']
    ordering_fields = ['delivery_date', 'quantity', 'id']
    ordering = ['-delivery_date']


class ExternalProductDeliveryRawMaterialViewSet(viewsets.ModelViewSet):
    queryset = ExternalProductDeliveryRawMaterial.objects.select_related(
        'delivery', 'raw_material'
    ).all()
    serializer_class = ExternalProductDeliveryRawMaterialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['delivery', 'raw_material']
    search_fields = ['raw_material__piece_name', 'raw_material__serial_number']
    ordering_fields = ['delivery_date', 'quantity', 'id']
    ordering = ['-delivery_date']


class ReturnedFromCustomerViewSet(viewsets.ModelViewSet):
    queryset = ReturnedFromCustomer.objects.select_related('received_by').all()
    serializer_class = ReturnedFromCustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['received_by']
    search_fields = ['customer_name', 'product_name', 'product_serial_number', 'product_part_number', 'product_item_code']
    ordering_fields = ['return_date', 'customer_name', 'id']
    ordering = ['-return_date']

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export محصولات برگشتی از مشتری به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_returned_from_customer(queryset)


class BorrowedProductViewSet(viewsets.ModelViewSet):
    queryset = BorrowedProduct.objects.all()
    serializer_class = BorrowedProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_name', 'serial_number', 'giver_company', 'receiver_person']
    ordering_fields = ['delivery_date', 'product_name', 'id']
    ordering = ['-delivery_date']

    @action(detail=False, methods=['get'])
    def pending_return(self, request):
        """امانی‌هایی که هنوز برگشت داده نشده‌اند"""
        pending_borrowed = self.queryset.filter(return_date__isnull=True)
        serializer = self.get_serializer(pending_borrowed, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Export محصولات قرضی به Excel"""
        queryset = self.filter_queryset(self.get_queryset())
        return WarehouseExcelExporter.export_borrowed_products(queryset)
