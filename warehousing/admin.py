from django.contrib import admin, messages
from django.http import HttpRequest
from django.utils.html import format_html
from jalali_date import date2jalali
# from import_export.admin import ImportExportModelAdmin
from .models import (
    QuarantineWarehouse,
    RawMaterialWarehouse,
    ProductWarehouse,
    ProductRawMaterial,
    ReturnedProduct,
    ResponsibleForTesting,
    ResponsibleForQC,
    ProductCode,
    ProductPart,
    SecondryWarehouse,
    SecondryWarehouseRawMaterial,
    ProductSecondryProduct,
    ProductDelivery,
    ProductDeliveryProduct,
    ProductDeliverySecondryProduct,
    ProductDeliveryRawMaterial,
    ReturnedFromCustomer,
    ExternalProductDelivery,
    ExternalProductDeliveryProduct,
    ExternalProductDeliverySecondryProduct,
    ExternalProductDeliveryRawMaterial,
    BorrowedProduct,
    Category
)

# گروه مجاز برای افزودن داده
ALLOWED_GROUP = 'warehouse_creators'
class ReadOnlyUnlessSuperuser(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.groups.filter(name=ALLOWED_GROUP).exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name=ALLOWED_GROUP).exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name=ALLOWED_GROUP).exists() 

# ====== action ======
@admin.action(description="انتقال به انبار مواد اولیه")
def transfer_to_raw_material(modeladmin, request, queryset):
    transferred, skipped = 0, 0
    for item in queryset:
        if item.test_date and item.qc_date and item.destination != 'raw_material':
            rawMaterial = RawMaterialWarehouse.objects.create(
                quarantine_reference=item,
                piece_name=item.piece_name,
                item_code=item.item_code,
                part_number=item.part_number,
                quantity=item.quantity,
                entry_date=item.exit_date or item.qc_date,
                price=item.unit_price,
                unit=item.unit,
                serial_number=item.serial_number,
                created_by=item.created_by,
            )
            item.destination = 'raw_material'
            rawMaterial.category.set(item.category.all())
            item.save()
            rawMaterial.save()
            transferred += 1
        else:
            skipped += 1
    if transferred:
        messages.success(request, f"{transferred} قطعه منتقل شد.")
    if skipped:
        messages.warning(request, f"{skipped} قطعه نادیده گرفته شد.")

@admin.action(description="انتقال به انبار بازگشت به فروشنده")
def send_to_returned_products(modeladmin, request, queryset):
    transferred, already_returned = 0, 0
    for item in queryset:
        if item.destination != 'returned':
            ReturnedProduct.objects.create(
                piece_name=item.piece_name,
                item_code=item.item_code,
                part_number=item.part_number,
                supplier=item.supplier,
                return_date=item.exit_date or item.qc_date or item.test_date or item.entry_date,
                reason_for_return=item.qc_description or item.test_description or "نامشخص",
                price=item.unit_price,
                unit=item.unit,
                serial_number=item.serial_number,
                created_by=item.created_by,
            )
            item.destination = 'returned'
            item.save()
            transferred += 1
        else:
            already_returned += 1
    if transferred:
        messages.success(request, f"{transferred} قطعه به انبار بازگشت به فروشنده منتقل شد.")
    if already_returned:
        messages.warning(request, f"{already_returned} قبلاً منتقل شده بودند.")

# ====== admin models======
@admin.register(QuarantineWarehouse)
class QuarantineWarehouseAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='تاریخ ورود')
    def j_entry_date(self, obj):
        return date2jalali(obj.entry_date) if obj.entry_date else "-"

    @admin.display(description='تاریخ تست')
    def j_test_date(self, obj):
        return date2jalali(obj.test_date) if obj.test_date else "-"

    @admin.display(description='تاریخ QC')
    def j_qc_date(self, obj):
        return date2jalali(obj.qc_date) if obj.qc_date else "-"

    @admin.display(description="وضعیت", ordering="status")
    def colored_status(self, obj):
        if obj.status == 'used_in_product':
            color, label = 'blue', 'استفاده شده در محصول'
        elif obj.status == 'used_in_secondry_warehouse':
            color, label = 'brown','استفاده شده در انبار ثانویه'
        elif obj.status == "rejected":
            color, label = 'red','رد شده'
        elif obj.status == 'inCompany':
            color, label = 'gold','تحویل افراد شرکت'
        elif obj.status == 'outCompany':
            color, label = 'teal','امانی شرکت به بیرون'
        elif (obj.destination == 'raw_material') or (obj.status=="transferred"):
            color, label = 'green', 'منتقل شده به مواد اولیه'
        elif obj.destination == 'returned':
            color, label = 'pink', 'منتقل شده به بازگشتی'
        elif not obj.test_date and not obj.qc_date:
            color, label = 'orange', 'در انتظار تست و QC'
        
        else:
            color, label = 'gray', 'در حال بررسی'
        return format_html('<span style="background-color:{}; color:white; padding:2px 6px; border-radius:4px;">{}</span>', color, label)

    @admin.display(description='دسته بندی')
    def get_category(self, obj):
        return ", ".join([cat.name for cat in obj.category.all()])


    list_display = (
        'piece_name', 'status_amani', 'item_code','part_number','serial_number','get_category', 'quantity',
        'j_entry_date', 'supplier', 'j_test_date', 'j_qc_date', 'destination', 'created_by', 'colored_status'
    )
    list_filter = ('piece_name', 'status_amani','item_code__product_code', 'part_number__product_part','serial_number', 'destination', 'category__name','status')
    search_fields = ('piece_name', 'status_amani','item_code__product_code', 'serial_number', 'part_number__product_part', 'supplier', 'category__name','status')
    ordering = ['-entry_date']
    actions = [transfer_to_raw_material, send_to_returned_products]

@admin.register(RawMaterialWarehouse)
class RawMaterialWarehouseAdmin(ReadOnlyUnlessSuperuser):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(quantity__gt=0)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='تاریخ ورود')
    def j_entry_date(self, obj):
        return date2jalali(obj.entry_date) if obj.entry_date else "-"

    @admin.display(description='دسته بندی')
    def get_category(self, obj):
        return ", ".join([cat.name for cat in obj.category.all()])

    list_display = (
        'piece_name', 'item_code', 'part_number', 'serial_number', 'get_category', 'quantity',
        'j_entry_date', 'price', 'unit', 'serial_number', 'created_by'
    )
    list_filter = ('piece_name', 'item_code__product_code', 'part_number__product_part','serial_number', 'category__name')
    search_fields = ('piece_name', 'item_code__product_code', 'part_number__product_part', 'serial_number', 'category__name')
    ordering = ['-entry_date']

class ProductRawMaterialInline(admin.TabularInline):
    model = ProductRawMaterial
    extra = 1
    fields = ['raw_material_source', 'quantity', 'user_who_used']
    readonly_fields = [
        'raw_material_name', 'item_code', 'part_number',
        'raw_material_entry_date', 'raw_material_price',
        'unit', 'serial_number',
    ]


@admin.register(ReturnedProduct)
class ReturnedProductAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='تاریخ بازگشت')
    def j_return_date(self, obj):
        return date2jalali(obj.return_date) if obj.return_date else "-"

    list_display = (
        'piece_name', 'item_code', 'part_number',
        'j_return_date', 'supplier', 'created_by'
    )
    search_fields = ('piece_name', 'item_code__product_code', 'part_number__product_part', 'serial_number')
    ordering = ['-return_date']

@admin.register(ResponsibleForTesting)
class ResponsibleForTestingAdmin(admin.ModelAdmin):
    list_display = ('first_last_name',)
    search_fields = ('first_last_name',)

@admin.register(ResponsibleForQC)
class ResponsibleForQCAdmin(admin.ModelAdmin):
    list_display = ('first_last_name',)
    search_fields = ('first_last_name',)

@admin.register(ProductCode)
class ProductCodeAdmin(ReadOnlyUnlessSuperuser):
    list_display = ('product_code',)
    search_fields = ('product_code',)

@admin.register(ProductPart)
class ProductPartAdmin(ReadOnlyUnlessSuperuser):
    list_display = ('product_part',)
    search_fields = ('product_part',)

class SecondryWarehouseRawMaterialInline(admin.TabularInline):
    model = SecondryWarehouseRawMaterial
    extra = 1
    fields = ['raw_material_source', 'quantity', 'user_who_used']

@admin.register(SecondryWarehouse)
class SecondryWarehouseAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    @admin.display(description="مواد انبار اولیه")
    def display_main_products(self, obj):
        try:
            return ", ".join([
                f"{item.raw_material_source.piece_name}-{item.raw_material_source.serial_number}-{item.raw_material_source.part_number}-(×{item.quantity})"
                for item in obj.raw_materials.all()
            ]) or "-"
        except:
            print("Please check database for delete raw material")
            
    @admin.display(description='تاریخ شروع ساخت')
    def j_start(self, obj):
        return date2jalali(obj.manufacturing_start_date) if obj.manufacturing_start_date else "-"

    @admin.display(description='تاریخ اتمام ساخت')
    def j_end(self, obj):
        return date2jalali(obj.manufacturing_end_date) if obj.manufacturing_end_date else "-"

    @admin.display(description='تاریخ شروع تست و QC')
    def j_test_qc_start(self, obj):
        return date2jalali(obj.test_qc_start_date) if obj.test_qc_start_date else "-"

    @admin.display(description='تاریخ پایان تست و QC')
    def j_test_qc_end(self, obj):
        return date2jalali(obj.test_qc_end_date) if obj.test_qc_end_date else "-"

    @admin.display(description='تاریخ خروج محصول')
    def j_exit(self, obj):
        return date2jalali(obj.product_exit_date) if obj.product_exit_date else "-"

    @admin.display(description="وضعیت", ordering="status")
    def colored_status(self, obj):
        if obj.status == 'secondry_warehouse':
            color, label = 'green', 'انبار ثانویه'
        elif obj.status == 'in_product':
            color, label = 'blue', 'استفاده شده در محصول'
        elif obj.status == 'internal_product':
            color, label = 'purple', 'تحویل افراد درون شرکت'
        elif obj.status == "out_product":
            color, label = 'teal', 'امانی شرکت به بیرون'
        elif obj.status == 'seller_product':
            color, label = 'gold', 'فروخته شده'
        else:
            color, label = 'gray', 'نامشخص'

        return format_html('<span style="background-color:{}; color:white; padding:2px 6px; border-radius:4px;">{}</span>', color, label)

    

    list_display = (
        'product_name', 'product_serial_number',
        'j_start','display_main_products','j_end',
        'j_test_qc_start', 'j_test_qc_end',
        'j_exit', 'exit_type', 'created_by','colored_status'
    )
    list_filter = ('product_name', 'product_serial_number', 'exit_type', 'created_by',)
    search_fields = ('product_name', 'product_serial_number')
    ordering = ['-manufacturing_start_date']
    inlines = [SecondryWarehouseRawMaterialInline]

class ProductSecondryProductInline(admin.TabularInline):
        model = ProductSecondryProduct
        extra = 1
        fields = ['secondry_product', 'quantity']


@admin.register(ProductWarehouse)
class ProductWarehouseAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    @admin.display(description="مواد انبار اولیه")
    def display_raw_products(self, obj):
        try:
            return ", ".join([
                f"{item.raw_material_source.piece_name}-{item.raw_material_source.serial_number}-{item.raw_material_source.part_number}-(×{item.quantity})"
                for item in obj.raw_materials.all()
            ]) or "-"
        except:
            print("Please check database for delete raw material")
    
    @admin.display(description="وضعیت", ordering="status")
    def colored_status(self, obj):
        if obj.status == 'product_warehouse':
            color, label = 'green', 'انبار محصولات'
        elif obj.status == 'internal_product':
            color, label = 'blue','تحویل افراد درون شرکت'
        elif obj.status == "out_product":
            color, label = 'teal','امانی شرکت به بیرون'
        elif obj.status == 'seller_product':
            color, label = 'gold','فروخته شده'

        return format_html('<span style="background-color:{}; color:white; padding:2px 6px; border-radius:4px;">{}</span>', color, label)

    
    
    @admin.display(description="محصولات ثانویه")
    def display_secondary_products(self, obj):
        return ", ".join([
            f"{item.secondry_product.product_name}-{item.secondry_product.product_serial_number}-(×{item.quantity})"
            for item in obj.secondry_products.all()
        ]) or "-"
    @admin.display(description='تاریخ شروع ساخت')
    def j_start(self, obj):
        return date2jalali(obj.manufacturing_start_date) if obj.manufacturing_start_date else "-"

    @admin.display(description='تاریخ اتمام ساخت')
    def j_end(self, obj):
        return date2jalali(obj.manufacturing_end_date) if obj.manufacturing_end_date else "-"

    @admin.display(description='تاریخ شروع تست و QC')
    def j_test_qc_start(self, obj):
        return date2jalali(obj.test_qc_start_date) if obj.test_qc_start_date else "-"

    @admin.display(description='تاریخ پایان تست و QC')
    def j_test_qc_end(self, obj):
        return date2jalali(obj.test_qc_end_date) if obj.test_qc_end_date else "-"

    @admin.display(description='تاریخ خروج محصول')
    def j_exit(self, obj):
        return date2jalali(obj.product_exit_date) if obj.product_exit_date else "-"

    list_display = (
        'product_name', 'product_serial_number','quantity',
        'j_start','display_raw_products','display_secondary_products' , 'j_end',
        'j_test_qc_start', 'j_test_qc_end',
        'j_exit', 'exit_type', 'created_by','colored_status'
    )
    list_filter = ('product_name','product_serial_number','status')
    search_fields = ('product_name', 'product_serial_number')
    ordering = ['-manufacturing_start_date']
    inlines = [ProductRawMaterialInline, ProductSecondryProductInline]

@admin.register(ProductDelivery)
class ProductDeliveryAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.deliverer = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description="محصولات اصلی")
    def display_main_products(self, obj):
        return ", ".join([
            f"{item.product.product_name} (×{item.quantity})"
            for item in obj.product_items.all()
        ]) or "-"

    @admin.display(description="محصولات ثانویه")
    def display_secondary_products(self, obj):
        return ", ".join([
            f"{item.secondry_product.product_name} (×{item.quantity})"
            for item in obj.secondry_items.all()
        ]) or "-"

    @admin.display(description="مواد اولیه")
    def display_raw_materials(self, obj):
        return ", ".join([
            f"{item.raw_material.piece_name} (×{item.quantity})"
            for item in obj.raw_material_items.all()
        ]) or "-"

    @admin.display(description='تاریخ تحویل')
    def j_delivery_date(self, obj):
        return date2jalali(obj.delivery_date) if obj.delivery_date else "-"

    @admin.display(description='تاریخ بازگشت')
    def j_return_date(self, obj):
        return date2jalali(obj.return_date) if obj.return_date else "-"

    list_display = (
        'receiver_name',
        'user_name',
        'j_delivery_date',
        'j_return_date',
        'deliverer',
        'display_main_products',
        'display_secondary_products',
        'display_raw_materials',
    )

    search_fields = ('receiver_name','user_name',)
    list_filter = ('receiver_name','user_name',)
    ordering = ['-delivery_date']
    inlines = [
        type('ProductDeliveryProductInline', (admin.TabularInline,), {
            'model': ProductDeliveryProduct,
            'extra': 1,
            'fields':('product','quantity','delivery_date','return_date')
        }),
        type('ProductDeliverySecondryProductInline', (admin.TabularInline,), {
            'model': ProductDeliverySecondryProduct,
            'extra': 1,
        }),
        type('ProductDeliveryRawMaterialInline', (admin.TabularInline,), {
            'model': ProductDeliveryRawMaterial,
            'extra': 1,
            'fields':('raw_material','quantity','delivery_date','return_date')
        }),
    ]

class ExternalProductDeliveryProductInline(admin.TabularInline):
    model = ExternalProductDeliveryProduct
    extra = 1

class ExternalProductDeliverySecondryProductInline(admin.TabularInline):
    model = ExternalProductDeliverySecondryProduct
    extra = 1

class ExternalProductDeliveryRawMaterialInline(admin.TabularInline):
    model = ExternalProductDeliveryRawMaterial
    extra = 1
    fields=('raw_material','quantity','delivery_date','return_date')

@admin.register(ExternalProductDelivery)
class ExternalProductDeliveryAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    @admin.display(description="محصولات اصلی")
    def display_main_products(self, obj):
        return ", ".join([
            f"{item.product.product_name}-{item.product.product_serial_number}-(×{item.quantity})"
            for item in obj.product_items.all()
        ]) or "-"

    @admin.display(description="محصولات ثانویه")
    def display_secondary_products(self, obj):
        return ", ".join([
            f"{item.secondry_product.product_name}-{item.secondry_product.product_serial_number}-(×{item.quantity})"
            for item in obj.secondry_items.all()
        ]) or "-"

    @admin.display(description="مواد اولیه")
    def display_raw_materials(self, obj):
        return ", ".join([
            f"{item.raw_material.piece_name}-{item.raw_material.serial_number}-{item.raw_material.part_number}-(×{item.quantity})"
            for item in obj.raw_material_items.all()
        ]) or "-"
    
    @admin.display(description="تاریخ تحویل")
    def j_delivery_date(self, obj):
        return date2jalali(obj.delivery_date) if obj.delivery_date else "-"

    @admin.display(description="تاریخ بازگشت")
    def j_return_date(self, obj):
        return date2jalali(obj.return_date) if obj.return_date else "-"

    list_display = (
        'receiver_name', 'j_delivery_date', 'j_return_date','display_main_products','display_secondary_products','display_raw_materials', 'deliverer'
    )
    search_fields = ('receiver_name',)
    ordering = ['-delivery_date']
    inlines = [
        ExternalProductDeliveryProductInline,
        ExternalProductDeliverySecondryProductInline,
        ExternalProductDeliveryRawMaterialInline
    ]

@admin.register(ReturnedFromCustomer)
class ReturnedFromCustomerAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    @admin.display(description='تاریخ بازگشت')
    def j_return_date(self, obj):
        return date2jalali(obj.return_date) if obj.return_date else "-"

    list_display = (
        'customer_name',
        'product_name',
        'product_serial_number',
        'product_part_number',
        'product_item_code',
        'j_return_date',
        'received_by',
    )
    search_fields = ('customer_name', 'product_name', 'product_part_number', 'product_item_code', 'product_serial_number')
    list_filter = ('customer_name', 'product_name', 'product_part_number', 'product_item_code', 'product_serial_number')
    ordering = ['-return_date']

@admin.register(BorrowedProduct)
class BorrowedProductAdmin(ReadOnlyUnlessSuperuser):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description="تاریخ تحویل")
    def j_delivery_date(self, obj):
        return date2jalali(obj.delivery_date) if obj.delivery_date else "-"

    @admin.display(description="تاریخ بازگرداندن")
    def j_return_date(self, obj):
        return date2jalali(obj.return_date) if obj.return_date else "-"

    list_display = (
        'product_name', 'serial_number', 'giver_company', 'receiver_person', 'j_delivery_date', 'j_return_date'
    )
    search_fields = ('product_name', 'serial_number', 'giver_company', 'receiver_person')
    ordering = ['-delivery_date']

@admin.register(Category)
class CategoryAdmin(ReadOnlyUnlessSuperuser):

    list_display = (
        'name', 'code', 'is_sub', 'sub_cat__name'
    )
    search_fields = ('name', 'code', 'is_sub', 'sub_cat__name')
    
