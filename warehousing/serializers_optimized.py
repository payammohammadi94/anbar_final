from rest_framework import serializers
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'code', 'is_sub', 'sub_cat']


class CategoryDetailSerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'code', 'is_sub', 'sub_cat', 'sub_categories']
    
    def get_sub_categories(self, obj):
        sub_cats = obj.catgory.all()
        return CategorySerializer(sub_cats, many=True).data


class ResponsibleForTestingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleForTesting
        fields = ['id', 'first_last_name']


class ResponsibleForQCSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleForQC
        fields = ['id', 'first_last_name']


class ProductPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPart
        fields = ['id', 'product_part']


class ProductCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCode
        fields = ['id', 'product_code']


class QuarantineWarehouseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    part_number = ProductPartSerializer(read_only=True)
    item_code = ProductCodeSerializer(read_only=True)
    qc_responsible = ResponsibleForQCSerializer(read_only=True)
    test_responsible = ResponsibleForTestingSerializer(read_only=True)
    
    # برای نوشتن
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    part_number_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    item_code_id = serializers.IntegerField(write_only=True, required=False)
    qc_responsible_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    test_responsible_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = QuarantineWarehouse
        fields = [
            'id', 'piece_name', 'category', 'part_number', 'item_code',
            'quantity', 'Meterage', 'entry_date', 'unit_price', 'unit', 'supplier',
            'serial_number', 'status', 'qc_date', 'qc_responsible', 'qc_description',
            'test_date', 'test_responsible', 'test_description', 'exit_date', 'destination',
            'category_ids', 'part_number_id', 'item_code_id', 'qc_responsible_id', 'test_responsible_id'
        ]
    
    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        part_number_id = validated_data.pop('part_number_id', None)
        item_code_id = validated_data.pop('item_code_id', None)
        qc_responsible_id = validated_data.pop('qc_responsible_id', None)
        test_responsible_id = validated_data.pop('test_responsible_id', None)
        
        instance = QuarantineWarehouse.objects.create(**validated_data)
        
        if category_ids:
            instance.category.set(category_ids)
        if part_number_id:
            instance.part_number_id = part_number_id
        if item_code_id:
            instance.item_code_id = item_code_id
        if qc_responsible_id:
            instance.qc_responsible_id = qc_responsible_id
        if test_responsible_id:
            instance.test_responsible_id = test_responsible_id
        
        instance.save()
        return instance


class RawMaterialWarehouseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    part_number = ProductPartSerializer(read_only=True)
    item_code = ProductCodeSerializer(read_only=True)
    
    # برای نوشتن
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    part_number_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    item_code_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = RawMaterialWarehouse
        fields = [
            'id', 'piece_name', 'category', 'part_number', 'item_code', 
            'quantity', 'entry_date', 'price', 'unit', 'serial_number',
            'category_ids', 'part_number_id', 'item_code_id'
        ]


class ProductWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductWarehouse
        fields = [
            'id', 'product_name', 'product_serial_number',
            'manufacturing_start_date', 'manufacturing_end_date', 'test_qc_start_date',
            'qc_responsible', 'test_approver', 'test_qc_end_date', 'product_exit_date',
            'exit_type', 'deliverer', 'receiver', 'finished_price'
        ]


class ProductWarehouseDetailSerializer(serializers.ModelSerializer):
    raw_materials = serializers.SerializerMethodField()
    secondry_products = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductWarehouse
        fields = [
            'id', 'product_name', 'product_serial_number',
            'manufacturing_start_date', 'manufacturing_end_date', 'test_qc_start_date',
            'qc_responsible', 'test_approver', 'test_qc_end_date', 'product_exit_date',
            'exit_type', 'deliverer', 'receiver', 'finished_price', 'raw_materials', 'secondry_products'
        ]
    
    def get_raw_materials(self, obj):
        raw_materials = obj.raw_materials.all()[:10]  # محدود کردن تعداد
        return ProductRawMaterialSerializer(raw_materials, many=True).data
    
    def get_secondry_products(self, obj):
        secondry_products = obj.secondry_products.all()[:10]  # محدود کردن تعداد
        return ProductSecondryProductSerializer(secondry_products, many=True).data


class ReturnedProductSerializer(serializers.ModelSerializer):
    part_number = ProductPartSerializer(read_only=True)
    item_code = ProductCodeSerializer(read_only=True)
    
    # برای نوشتن
    part_number_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    item_code_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ReturnedProduct
        fields = [
            'id', 'piece_name', 'part_number', 'item_code',
            'supplier', 'return_date', 'reason_for_return', 'price', 'unit', 'serial_number',
            'part_number_id', 'item_code_id'
        ]


class ProductRawMaterialSerializer(serializers.ModelSerializer):
    product = ProductWarehouseSerializer(read_only=True)
    part_number = ProductPartSerializer(read_only=True)
    item_code = ProductCodeSerializer(read_only=True)
    
    # برای نوشتن
    product_id = serializers.IntegerField(write_only=True, required=False)
    part_number_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    item_code_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProductRawMaterial
        fields = [
            'id', 'product', 'raw_material_name', 'part_number', 'item_code', 
            'quantity', 'user_who_used', 'raw_material_entry_date', 'raw_material_price', 
            'unit', 'serial_number', 'product_id', 'part_number_id', 'item_code_id'
        ]


class SecondryWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondryWarehouse
        fields = [
            'id', 'product_name', 'product_serial_number',
            'manufacturing_start_date', 'manufacturing_end_date', 'test_qc_start_date',
            'test_qc_end_date', 'test_approver', 'qc_responsible', 'product_exit_date',
            'exit_type', 'deliverer', 'receiver', 'finished_price'
        ]


class SecondryWarehouseRawMaterialSerializer(serializers.ModelSerializer):
    secondryWarehouse = SecondryWarehouseSerializer(read_only=True)
    part_number = ProductPartSerializer(read_only=True)
    item_code = ProductCodeSerializer(read_only=True)
    
    # برای نوشتن
    secondryWarehouse_id = serializers.IntegerField(write_only=True, required=False)
    part_number_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    item_code_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = SecondryWarehouseRawMaterial
        fields = [
            'id', 'secondryWarehouse', 'raw_material_name', 'part_number', 'item_code', 
            'serial_number', 'quantity', 'user_who_used', 'raw_material_entry_date', 
            'raw_material_price', 'unit', 'secondryWarehouse_id', 'part_number_id', 'item_code_id'
        ]


class ProductSecondryProductSerializer(serializers.ModelSerializer):
    product = ProductWarehouseSerializer(read_only=True)
    secondry_product = SecondryWarehouseSerializer(read_only=True)
    
    # برای نوشتن
    product_id = serializers.IntegerField(write_only=True, required=False)
    secondry_product_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProductSecondryProduct
        fields = ['id', 'product', 'secondry_product', 'quantity', 'product_id', 'secondry_product_id']


class ProductDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDelivery
        fields = [
            'id', 'receiver_name', 'user_name', 'delivery_date', 'return_date'
        ]


class ProductDeliveryDetailSerializer(serializers.ModelSerializer):
    product_items = serializers.SerializerMethodField()
    secondry_items = serializers.SerializerMethodField()
    raw_material_items = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductDelivery
        fields = [
            'id', 'receiver_name', 'user_name', 'delivery_date', 'return_date',
            'product_items', 'secondry_items', 'raw_material_items'
        ]
    
    def get_product_items(self, obj):
        product_items = obj.product_items.all()[:10]  # محدود کردن تعداد
        return ProductDeliveryProductSerializer(product_items, many=True).data
    
    def get_secondry_items(self, obj):
        secondry_items = obj.secondry_items.all()[:10]  # محدود کردن تعداد
        return ProductDeliverySecondryProductSerializer(secondry_items, many=True).data
    
    def get_raw_material_items(self, obj):
        raw_material_items = obj.raw_material_items.all()[:10]  # محدود کردن تعداد
        return ProductDeliveryRawMaterialSerializer(raw_material_items, many=True).data


class ProductDeliveryProductSerializer(serializers.ModelSerializer):
    product = ProductWarehouseSerializer(read_only=True)
    
    # برای نوشتن
    product_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProductDeliveryProduct
        fields = [
            'id', 'product', 'quantity', 'delivery_date', 'return_date', 'product_id'
        ]


class ProductDeliverySecondryProductSerializer(serializers.ModelSerializer):
    secondry_product = SecondryWarehouseSerializer(read_only=True)
    
    # برای نوشتن
    secondry_product_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProductDeliverySecondryProduct
        fields = [
            'id', 'secondry_product', 'quantity', 'delivery_date', 'return_date', 'secondry_product_id'
        ]


class ProductDeliveryRawMaterialSerializer(serializers.ModelSerializer):
    part_number = ProductPartSerializer(read_only=True)
    item_code = ProductCodeSerializer(read_only=True)
    
    # برای نوشتن
    part_number_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    item_code_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProductDeliveryRawMaterial
        fields = [
            'id', 'quantity', 'delivery_date', 'return_date', 'raw_material_name', 
            'part_number', 'item_code', 'serial_number', 'user_who_used',
            'raw_material_entry_date', 'raw_material_price', 'unit', 
            'part_number_id', 'item_code_id'
        ]


class ExternalProductDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalProductDelivery
        fields = [
            'id', 'receiver_name', 'delivery_date', 'return_date', 'reference_letter'
        ]


class ExternalProductDeliveryProductSerializer(serializers.ModelSerializer):
    product = ProductWarehouseSerializer(read_only=True)
    
    # برای نوشتن
    product_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ExternalProductDeliveryProduct
        fields = [
            'id', 'product', 'quantity', 'delivery_date', 'return_date', 'product_id'
        ]


class ExternalProductDeliverySecondryProductSerializer(serializers.ModelSerializer):
    secondry_product = SecondryWarehouseSerializer(read_only=True)
    
    # برای نوشتن
    secondry_product_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ExternalProductDeliverySecondryProduct
        fields = [
            'id', 'secondry_product', 'quantity', 'delivery_date', 'return_date', 'secondry_product_id'
        ]


class ExternalProductDeliveryRawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalProductDeliveryRawMaterial
        fields = [
            'id', 'quantity', 'delivery_date', 'return_date'
        ]


class ReturnedFromCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnedFromCustomer
        fields = [
            'id', 'customer_name', 'product_name', 'product_serial_number',
            'product_part_number', 'product_item_code', 'return_reason', 'return_date'
        ]


class BorrowedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedProduct
        fields = [
            'id', 'product_name', 'serial_number', 'giver_company',
            'receiver_person', 'delivery_date', 'return_date'
        ]


