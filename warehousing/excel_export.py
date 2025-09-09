import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from django.db.models import QuerySet
from typing import List, Dict, Any
import json


class ExcelExporter:
    """کلاس برای export داده‌ها به Excel"""
    
    @staticmethod
    def export_to_excel(queryset: QuerySet, filename: str, fields: List[str] = None) -> HttpResponse:
        """
        Export queryset به Excel
        
        Args:
            queryset: QuerySet Django
            filename: نام فایل Excel
            fields: لیست فیلدهای مورد نظر (اختیاری)
        
        Returns:
            HttpResponse با فایل Excel
        """
        # تبدیل QuerySet به لیست دیکشنری
        data = list(queryset.values())
        
        if not data:
            # اگر داده‌ای وجود ندارد، یک DataFrame خالی ایجاد کن
            df = pd.DataFrame(columns=fields or [])
        else:
            # ایجاد DataFrame
            df = pd.DataFrame(data)
            
            # اگر فیلدهای خاصی مشخص شده، فقط آن‌ها را انتخاب کن
            if fields:
                available_fields = [field for field in fields if field in df.columns]
                df = df[available_fields]
        
        # ایجاد فایل Excel در memory
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
            
            # تنظیم عرض ستون‌ها
            worksheet = writer.sheets['Data']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        # تنظیم response
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        
        return response
    
    @staticmethod
    def export_multiple_sheets(data_dict: Dict[str, QuerySet], filename: str) -> HttpResponse:
        """
        Export چندین QuerySet به Excel با sheet های مختلف
        
        Args:
            data_dict: دیکشنری با نام sheet و QuerySet
            filename: نام فایل Excel
        
        Returns:
            HttpResponse با فایل Excel
        """
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for sheet_name, queryset in data_dict.items():
                data = list(queryset.values())
                
                if data:
                    df = pd.DataFrame(data)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    
                    # تنظیم عرض ستون‌ها
                    worksheet = writer.sheets[sheet_name]
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        
                        for cell in column:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        
                        adjusted_width = min(max_length + 2, 50)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        
        return response
    
    @staticmethod
    def export_with_relations(queryset: QuerySet, filename: str, 
                            relation_fields: Dict[str, str] = None) -> HttpResponse:
        """
        Export با روابط (relations)
        
        Args:
            queryset: QuerySet Django
            filename: نام فایل Excel
            relation_fields: دیکشنری فیلدهای relation
        
        Returns:
            HttpResponse با فایل Excel
        """
        data = []
        
        for obj in queryset:
            obj_data = {}
            
            # فیلدهای عادی
            for field in obj._meta.fields:
                value = getattr(obj, field.name)
                if hasattr(value, 'pk'):
                    obj_data[field.name] = str(value)
                else:
                    obj_data[field.name] = value
            
            # فیلدهای relation
            if relation_fields:
                for field_name, display_field in relation_fields.items():
                    if hasattr(obj, field_name):
                        related_obj = getattr(obj, field_name)
                        if related_obj:
                            if hasattr(related_obj, display_field):
                                obj_data[f"{field_name}_{display_field}"] = getattr(related_obj, display_field)
                            else:
                                obj_data[f"{field_name}_{display_field}"] = str(related_obj)
                        else:
                            obj_data[f"{field_name}_{display_field}"] = ""
            
            data.append(obj_data)
        
        df = pd.DataFrame(data)
        
        # ایجاد فایل Excel
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
            
            # تنظیم عرض ستون‌ها
            worksheet = writer.sheets['Data']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        
        return response


class WarehouseExcelExporter(ExcelExporter):
    """کلاس مخصوص export انبارها"""
    
    @staticmethod
    def export_quarantine_warehouse(queryset):
        """Export انبار قرنطینه"""
        relation_fields = {
            'part_number': 'product_part',
            'item_code': 'product_code',
            'qc_responsible': 'first_last_name',
            'test_responsible': 'first_last_name'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'quarantine_warehouse', relation_fields
        )
    
    @staticmethod
    def export_raw_material_warehouse(queryset):
        """Export انبار مواد اولیه"""
        relation_fields = {
            'part_number': 'product_part',
            'item_code': 'product_code'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'raw_material_warehouse', relation_fields
        )
    
    @staticmethod
    def export_product_warehouse(queryset):
        """Export انبار محصولات"""
        return WarehouseExcelExporter.export_to_excel(
            queryset, 'product_warehouse'
        )
    
    @staticmethod
    def export_secondry_warehouse(queryset):
        """Export انبار ثانویه"""
        return WarehouseExcelExporter.export_to_excel(
            queryset, 'secondry_warehouse'
        )
    
    @staticmethod
    def export_categories(queryset):
        """Export دسته‌بندی‌ها"""
        relation_fields = {
            'sub_cat': 'name'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'categories', relation_fields
        )
    
    @staticmethod
    def export_all_warehouses():
        """Export تمام انبارها در یک فایل"""
        from .models import (
            Category, ProductPart, ProductCode, QuarantineWarehouse, 
            RawMaterialWarehouse, ProductWarehouse, ReturnedProduct,
            SecondryWarehouse, ProductDelivery, ExternalProductDelivery,
            ReturnedFromCustomer, BorrowedProduct
        )
        
        data_dict = {
            'Categories': Category.objects.all(),
            'ProductParts': ProductPart.objects.all(),
            'ProductCodes': ProductCode.objects.all(),
            'Quarantine_Warehouse': QuarantineWarehouse.objects.all(),
            'Raw_Material_Warehouse': RawMaterialWarehouse.objects.all(),
            'Product_Warehouse': ProductWarehouse.objects.all(),
            'Returned_Products': ReturnedProduct.objects.all(),
            'Secondry_Warehouse': SecondryWarehouse.objects.all(),
            'Product_Delivery': ProductDelivery.objects.all(),
            'External_Product_Delivery': ExternalProductDelivery.objects.all(),
            'Returned_From_Customer': ReturnedFromCustomer.objects.all(),
            'Borrowed_Products': BorrowedProduct.objects.all()
        }
        
        return WarehouseExcelExporter.export_multiple_sheets(
            data_dict, 'all_warehouses'
        )
    
    @staticmethod
    def export_product_parts(queryset):
        """Export قطعات محصول"""
        return WarehouseExcelExporter.export_to_excel(
            queryset, 'product_parts'
        )
    
    @staticmethod
    def export_product_codes(queryset):
        """Export کدهای محصول"""
        return WarehouseExcelExporter.export_to_excel(
            queryset, 'product_codes'
        )
    
    @staticmethod
    def export_returned_products(queryset):
        """Export محصولات برگشتی"""
        relation_fields = {
            'part_number': 'product_part',
            'item_code': 'product_code'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'returned_products', relation_fields
        )
    
    @staticmethod
    def export_product_delivery(queryset):
        """Export تحویل محصولات"""
        return WarehouseExcelExporter.export_to_excel(
            queryset, 'product_delivery'
        )
    
    @staticmethod
    def export_external_product_delivery(queryset):
        """Export تحویل محصولات خارجی"""
        return WarehouseExcelExporter.export_to_excel(
            queryset, 'external_product_delivery'
        )
    
    @staticmethod
    def export_returned_from_customer(queryset):
        """Export محصولات برگشتی از مشتری"""
        return WarehouseExcelExporter.export_to_excel(
            queryset, 'returned_from_customer'
        )
    
    @staticmethod
    def export_borrowed_products(queryset):
        """Export محصولات قرضی"""
        return WarehouseExcelExporter.export_to_excel(
            queryset, 'borrowed_products'
        )
