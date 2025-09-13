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
                # استفاده از export_with_relations برای نمایش روابط
                # ایجاد sheet حتی اگر داده‌ای وجود نداشته باشد
                # تعریف روابط برای هر مدل
                relation_fields = {}
                many_to_many_fields = {}
                
                # تشخیص نوع مدل و تنظیم روابط
                model_name = queryset.model.__name__
                
                if model_name == 'QuarantineWarehouse':
                    relation_fields = {
                        'part_number': 'product_part',
                        'item_code': 'product_code',
                        'qc_responsible': 'first_last_name',
                        'test_responsible': 'first_last_name',
                        'created_by': 'username'
                    }
                    many_to_many_fields = {'category': 'name'}
                elif model_name == 'RawMaterialWarehouse':
                    relation_fields = {
                        'part_number': 'product_part',
                        'item_code': 'product_code',
                        'quarantine_reference': 'piece_name',
                        'created_by': 'username'
                    }
                    many_to_many_fields = {'category': 'name'}
                elif model_name == 'ProductWarehouse':
                    relation_fields = {'created_by': 'username'}
                elif model_name == 'SecondryWarehouse':
                    relation_fields = {'created_by': 'username'}
                elif model_name == 'ProductDelivery':
                    relation_fields = {'deliverer': 'username'}
                elif model_name == 'ExternalProductDelivery':
                    relation_fields = {'deliverer': 'username'}
                elif model_name == 'ReturnedFromCustomer':
                    relation_fields = {'received_by': 'username'}
                elif model_name == 'ReturnedProduct':
                    relation_fields = {
                        'part_number': 'product_part',
                        'item_code': 'product_code',
                        'created_by': 'username'
                    }
                elif model_name == 'ProductPart':
                    relation_fields = {'created_by': 'username'}
                elif model_name == 'ProductCode':
                    relation_fields = {'created_by': 'username'}
                elif model_name == 'Category':
                    relation_fields = {'sub_cat': 'name'}
                elif model_name == 'ResponsibleForTesting':
                    relation_fields = {'created_by': 'username'}
                elif model_name == 'ResponsibleForQC':
                    relation_fields = {'created_by': 'username'}
                elif model_name == 'ProductRawMaterial':
                    relation_fields = {
                        'product': 'product_name',
                        'raw_material_source': 'piece_name',
                        'part_number': 'product_part',
                        'item_code': 'product_code',
                        'created_by': 'username'
                    }
                elif model_name == 'SecondryWarehouseRawMaterial':
                    relation_fields = {
                        'secondryWarehouse': 'product_name',
                        'raw_material_source': 'piece_name',
                        'part_number': 'product_part',
                        'item_code': 'product_code',
                        'created_by': 'username'
                    }
                elif model_name == 'ProductSecondryProduct':
                    relation_fields = {
                        'product': 'product_name',
                        'secondry_product': 'product_name'
                    }
                elif model_name == 'ProductDeliveryProduct':
                    relation_fields = {
                        'delivery': 'receiver_name',
                        'product': 'product_name'
                    }
                elif model_name == 'ProductDeliverySecondryProduct':
                    relation_fields = {
                        'delivery': 'receiver_name',
                        'secondry_product': 'product_name'
                    }
                elif model_name == 'ProductDeliveryRawMaterial':
                    relation_fields = {
                        'delivery': 'receiver_name',
                        'raw_material': 'piece_name',
                        'part_number': 'product_part',
                        'item_code': 'product_code'
                    }
                elif model_name == 'ExternalProductDeliveryProduct':
                    relation_fields = {
                        'delivery': 'receiver_name',
                        'product': 'product_name'
                    }
                elif model_name == 'ExternalProductDeliverySecondryProduct':
                    relation_fields = {
                        'delivery': 'receiver_name',
                        'secondry_product': 'product_name'
                    }
                elif model_name == 'ExternalProductDeliveryRawMaterial':
                    relation_fields = {
                        'delivery': 'receiver_name',
                        'raw_material': 'piece_name',
                        'part_number': 'product_part',
                        'item_code': 'product_code'
                    }
                
                # استفاده از export_with_relations
                temp_response = ExcelExporter.export_with_relations(
                    queryset, f'temp_{sheet_name}', relation_fields, many_to_many_fields
                )
                
                # خواندن محتوای Excel و اضافه کردن به فایل اصلی
                temp_content = temp_response.content
                temp_df = pd.read_excel(BytesIO(temp_content))
                temp_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
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
                            relation_fields: Dict[str, str] = None,
                            many_to_many_fields: Dict[str, str] = None) -> HttpResponse:
        """
        Export با روابط (relations) شامل ForeignKey و ManyToMany
        
        Args:
            queryset: QuerySet Django
            filename: نام فایل Excel
            relation_fields: دیکشنری فیلدهای ForeignKey
            many_to_many_fields: دیکشنری فیلدهای ManyToMany
        
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
                    # برای ForeignKey، سعی کن نام یا مقدار قابل خواندن پیدا کنی
                    obj_data[field.name] = str(value)
                else:
                    obj_data[field.name] = value
            
            # فیلدهای ForeignKey
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
            
            # فیلدهای ManyToMany
            if many_to_many_fields:
                for field_name, display_field in many_to_many_fields.items():
                    if hasattr(obj, field_name):
                        related_objects = getattr(obj, field_name).all()
                        if related_objects:
                            values = []
                            for related_obj in related_objects:
                                if hasattr(related_obj, display_field):
                                    values.append(str(getattr(related_obj, display_field)))
                                else:
                                    values.append(str(related_obj))
                            obj_data[f"{field_name}_{display_field}"] = ", ".join(values)
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
            'test_responsible': 'first_last_name',
            'created_by': 'username'
        }
        many_to_many_fields = {
            'category': 'name'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'quarantine_warehouse', relation_fields, many_to_many_fields
        )
    
    @staticmethod
    def export_raw_material_warehouse(queryset):
        """Export انبار مواد اولیه"""
        relation_fields = {
            'part_number': 'product_part',
            'item_code': 'product_code',
            'quarantine_reference': 'piece_name',
            'created_by': 'username'
        }
        many_to_many_fields = {
            'category': 'name'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'raw_material_warehouse', relation_fields, many_to_many_fields
        )
    
    @staticmethod
    def export_product_warehouse(queryset):
        """Export انبار محصولات"""
        relation_fields = {
            'created_by': 'username'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'product_warehouse', relation_fields
        )
    
    @staticmethod
    def export_secondry_warehouse(queryset):
        """Export انبار ثانویه"""
        relation_fields = {
            'created_by': 'username'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'secondry_warehouse', relation_fields
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
        from datetime import datetime
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
        
        # ایجاد نام فایل با تاریخ و ساعت
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = f'all_warehouses_{timestamp}'
        
        data_dict = {
            'Categories': Category.objects.all(),
            'Responsible_For_Testing': ResponsibleForTesting.objects.all(),
            'Responsible_For_QC': ResponsibleForQC.objects.all(),
            'Product_Parts': ProductPart.objects.all(),
            'Product_Codes': ProductCode.objects.all(),
            'Quarantine_Warehouse': QuarantineWarehouse.objects.all(),
            'Raw_Material_Warehouse': RawMaterialWarehouse.objects.all(),
            'Product_Warehouse': ProductWarehouse.objects.all(),
            'Returned_Products': ReturnedProduct.objects.all(),
            'Product_Raw_Material': ProductRawMaterial.objects.all(),
            'Secondry_Warehouse': SecondryWarehouse.objects.all(),
            'Secondry_Warehouse_Raw_Material': SecondryWarehouseRawMaterial.objects.all(),
            'Product_Secondry_Product': ProductSecondryProduct.objects.all(),
            'Product_Delivery': ProductDelivery.objects.all(),
            'Product_Delivery_Product': ProductDeliveryProduct.objects.all(),
            'Product_Delivery_Secondry_Product': ProductDeliverySecondryProduct.objects.all(),
            'Product_Delivery_Raw_Material': ProductDeliveryRawMaterial.objects.all(),
            'External_Product_Delivery': ExternalProductDelivery.objects.all(),
            'External_Product_Delivery_Product': ExternalProductDeliveryProduct.objects.all(),
            'External_Product_Delivery_Secondry_Product': ExternalProductDeliverySecondryProduct.objects.all(),
            'External_Product_Delivery_Raw_Material': ExternalProductDeliveryRawMaterial.objects.all(),
            'Returned_From_Customer': ReturnedFromCustomer.objects.all(),
            'Borrowed_Products': BorrowedProduct.objects.all()
        }
        
        return WarehouseExcelExporter.export_multiple_sheets(
            data_dict, filename
        )
    
    @staticmethod
    def export_product_parts(queryset):
        """Export قطعات محصول"""
        relation_fields = {
            'created_by': 'username'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'product_parts', relation_fields
        )
    
    @staticmethod
    def export_product_codes(queryset):
        """Export کدهای محصول"""
        relation_fields = {
            'created_by': 'username'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'product_codes', relation_fields
        )
    
    @staticmethod
    def export_returned_products(queryset):
        """Export محصولات برگشتی"""
        relation_fields = {
            'part_number': 'product_part',
            'item_code': 'product_code',
            'created_by': 'username'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'returned_products', relation_fields
        )
    
    @staticmethod
    def export_product_delivery(queryset):
        """Export تحویل محصولات"""
        relation_fields = {
            'deliverer': 'username'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'product_delivery', relation_fields
        )
    
    @staticmethod
    def export_external_product_delivery(queryset):
        """Export تحویل محصولات خارجی"""
        relation_fields = {
            'deliverer': 'username'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'external_product_delivery', relation_fields
        )
    
    @staticmethod
    def export_returned_from_customer(queryset):
        """Export محصولات برگشتی از مشتری"""
        relation_fields = {
            'received_by': 'username'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'returned_from_customer', relation_fields
        )
    
    @staticmethod
    def export_borrowed_products(queryset):
        """Export محصولات قرضی"""
        return WarehouseExcelExporter.export_to_excel(
            queryset, 'borrowed_products'
        )
    
    @staticmethod
    def export_responsible_for_testing(queryset):
        """Export مسئولین تست"""
        relation_fields = {
            'created_by': 'username'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'responsible_for_testing', relation_fields
        )
    
    @staticmethod
    def export_responsible_for_qc(queryset):
        """Export مسئولین QC"""
        relation_fields = {
            'created_by': 'username'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'responsible_for_qc', relation_fields
        )
    
    @staticmethod
    def export_product_raw_material(queryset):
        """Export مواد اولیه محصول"""
        relation_fields = {
            'product': 'product_name',
            'raw_material_source': 'piece_name',
            'part_number': 'product_part',
            'item_code': 'product_code',
            'created_by': 'username'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'product_raw_material', relation_fields
        )
    
    @staticmethod
    def export_secondry_warehouse_raw_material(queryset):
        """Export مواد اولیه انبار ثانویه"""
        relation_fields = {
            'secondryWarehouse': 'product_name',
            'raw_material_source': 'piece_name',
            'part_number': 'product_part',
            'item_code': 'product_code',
            'created_by': 'username'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'secondry_warehouse_raw_material', relation_fields
        )
    
    @staticmethod
    def export_product_secondry_product(queryset):
        """Export محصولات ثانویه در محصول نهایی"""
        relation_fields = {
            'product': 'product_name',
            'secondry_product': 'product_name'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'product_secondry_product', relation_fields
        )
    
    @staticmethod
    def export_product_delivery_product(queryset):
        """Export محصولات تحویل افراد"""
        relation_fields = {
            'delivery': 'receiver_name',
            'product': 'product_name'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'product_delivery_product', relation_fields
        )
    
    @staticmethod
    def export_product_delivery_secondry_product(queryset):
        """Export محصولات ثانویه تحویل افراد"""
        relation_fields = {
            'delivery': 'receiver_name',
            'secondry_product': 'product_name'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'product_delivery_secondry_product', relation_fields
        )
    
    @staticmethod
    def export_product_delivery_raw_material(queryset):
        """Export مواد اولیه تحویل افراد"""
        relation_fields = {
            'delivery': 'receiver_name',
            'raw_material': 'piece_name',
            'part_number': 'product_part',
            'item_code': 'product_code'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'product_delivery_raw_material', relation_fields
        )
    
    @staticmethod
    def export_external_product_delivery_product(queryset):
        """Export محصولات امانی خارجی"""
        relation_fields = {
            'delivery': 'receiver_name',
            'product': 'product_name'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'external_product_delivery_product', relation_fields
        )
    
    @staticmethod
    def export_external_product_delivery_secondry_product(queryset):
        """Export محصولات ثانویه امانی خارجی"""
        relation_fields = {
            'delivery': 'receiver_name',
            'secondry_product': 'product_name'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'external_product_delivery_secondry_product', relation_fields
        )
    
    @staticmethod
    def export_external_product_delivery_raw_material(queryset):
        """Export مواد اولیه امانی خارجی"""
        relation_fields = {
            'delivery': 'receiver_name',
            'raw_material': 'piece_name',
            'part_number': 'product_part',
            'item_code': 'product_code'
        }
        return WarehouseExcelExporter.export_with_relations(
            queryset, 'external_product_delivery_raw_material', relation_fields
        )
