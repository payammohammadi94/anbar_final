from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

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

# Import all ViewSets
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

from .excel_export import WarehouseExcelExporter


def api_login_page(request):
    """صفحه لاگین مخصوص REST framework"""
    return render(request, 'warehousing/api_login.html')


@method_decorator(csrf_exempt, name='dispatch')
class APILoginView(View):
    """View برای لاگین API"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return JsonResponse({'error': 'نام کاربری و رمز عبور الزامی است'}, status=400)
            
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({'message': 'ورود موفقیت‌آمیز', 'user': user.username})
            else:
                return JsonResponse({'error': 'نام کاربری یا رمز عبور اشتباه است'}, status=401)
                
        except Exception as e:
            return JsonResponse({'error': 'خطا در پردازش درخواست'}, status=500)


class ExcelExportView(View):
    """View برای export تمام انبارها به Excel"""
    
    def get(self, request):
        """Export تمام انبارها به یک فایل Excel"""
        try:
            return WarehouseExcelExporter.export_all_warehouses()
        except Exception as e:
            return JsonResponse({'error': f'خطا در export: {str(e)}'}, status=500)