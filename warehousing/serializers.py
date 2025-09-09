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
    sub_categories = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'code', 'is_sub', 'sub_cat', 'sub_categories']
    
    def get_sub_categories(self, obj):
        sub_cats = obj.catgory.all()
        return CategorySerializer(sub_cats, many=True).data


class ResponsibleForTestingSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = ResponsibleForTesting
        fields = ['id', 'first_last_name', 'created_by']


class ResponsibleForQCSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = ResponsibleForQC
        fields = ['id', 'first_last_name', 'created_by']


class ProductPartSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = ProductPart
        fields = ['id', 'product_part', 'created_by']


class ProductCodeSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = ProductCode
        fields = ['id', 'product_code', 'created_by']


class QuarantineWarehouseSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
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
            'id', 'created_by', 'piece_name', 'category', 'part_number', 'item_code',
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
    
    def update(self, instance, validated_data):
        category_ids = validated_data.pop('category_ids', None)
        part_number_id = validated_data.pop('part_number_id', None)
        item_code_id = validated_data.pop('item_code_id', None)
        qc_responsible_id = validated_data.pop('qc_responsible_id', None)
        test_responsible_id = validated_data.pop('test_responsible_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if category_ids is not None:
            instance.category.set(category_ids)
        if part_number_id is not None:
            instance.part_number_id = part_number_id
        if item_code_id is not None:
            instance.item_code_id = item_code_id
        if qc_responsible_id is not None:
            instance.qc_responsible_id = qc_responsible_id
        if test_responsible_id is not None:
            instance.test_responsible_id = test_responsible_id
        
        instance.save()
        return instance


class RawMaterialWarehouseSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    quarantine_reference = QuarantineWarehouseSerializer(read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    part_number = ProductPartSerializer(read_only=True)
    item_code = ProductCodeSerializer(read_only=True)
    
    # برای نوشتن
    quarantine_reference_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
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
            'id', 'created_by', 'quarantine_reference', 'category', 'piece_name',
            'part_number', 'item_code', 'quantity', 'entry_date', 'price', 'unit',
            'serial_number', 'quarantine_reference_id', 'category_ids', 'part_number_id', 'item_code_id'
        ]
    
    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        quarantine_reference_id = validated_data.pop('quarantine_reference_id', None)
        part_number_id = validated_data.pop('part_number_id', None)
        item_code_id = validated_data.pop('item_code_id', None)
        
        instance = RawMaterialWarehouse.objects.create(**validated_data)
        
        if category_ids:
            instance.category.set(category_ids)
        if quarantine_reference_id:
            instance.quarantine_reference_id = quarantine_reference_id
        if part_number_id:
            instance.part_number_id = part_number_id
        if item_code_id:
            instance.item_code_id = item_code_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        category_ids = validated_data.pop('category_ids', None)
        quarantine_reference_id = validated_data.pop('quarantine_reference_id', None)
        part_number_id = validated_data.pop('part_number_id', None)
        item_code_id = validated_data.pop('item_code_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if category_ids is not None:
            instance.category.set(category_ids)
        if quarantine_reference_id is not None:
            instance.quarantine_reference_id = quarantine_reference_id
        if part_number_id is not None:
            instance.part_number_id = part_number_id
        if item_code_id is not None:
            instance.item_code_id = item_code_id
        
        instance.save()
        return instance


class ProductWarehouseSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    raw_materials = serializers.SerializerMethodField()
    secondry_products = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductWarehouse
        fields = [
            'id', 'created_by', 'product_name', 'product_serial_number',
            'manufacturing_start_date', 'manufacturing_end_date', 'test_qc_start_date',
            'qc_responsible', 'test_approver', 'test_qc_end_date', 'product_exit_date',
            'exit_type', 'deliverer', 'receiver', 'finished_price', 'raw_materials', 'secondry_products'
        ]
    
    def get_raw_materials(self, obj):
        raw_materials = obj.raw_materials.all()
        return ProductRawMaterialSerializer(raw_materials, many=True).data
    
    def get_secondry_products(self, obj):
        secondry_products = obj.secondry_products.all()
        return ProductSecondryProductSerializer(secondry_products, many=True).data


class ReturnedProductSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    part_number = ProductPartSerializer(read_only=True)
    item_code = ProductCodeSerializer(read_only=True)
    
    # برای نوشتن
    part_number_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    item_code_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ReturnedProduct
        fields = [
            'id', 'created_by', 'piece_name', 'part_number', 'item_code',
            'supplier', 'return_date', 'reason_for_return', 'price', 'unit', 'serial_number',
            'part_number_id', 'item_code_id'
        ]
    
    def create(self, validated_data):
        part_number_id = validated_data.pop('part_number_id', None)
        item_code_id = validated_data.pop('item_code_id', None)
        
        instance = ReturnedProduct.objects.create(**validated_data)
        
        if part_number_id:
            instance.part_number_id = part_number_id
        if item_code_id:
            instance.item_code_id = item_code_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        part_number_id = validated_data.pop('part_number_id', None)
        item_code_id = validated_data.pop('item_code_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if part_number_id is not None:
            instance.part_number_id = part_number_id
        if item_code_id is not None:
            instance.item_code_id = item_code_id
        
        instance.save()
        return instance


class ProductRawMaterialSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    product = ProductWarehouseSerializer(read_only=True)
    raw_material_source = RawMaterialWarehouseSerializer(read_only=True)
    part_number = ProductPartSerializer(read_only=True)
    item_code = ProductCodeSerializer(read_only=True)
    
    # برای نوشتن
    product_id = serializers.IntegerField(write_only=True, required=False)
    raw_material_source_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    part_number_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    item_code_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProductRawMaterial
        fields = [
            'id', 'created_by', 'product', 'raw_material_source', 'raw_material_name',
            'part_number', 'item_code', 'quantity', 'user_who_used', 'raw_material_entry_date',
            'raw_material_price', 'unit', 'serial_number', 'product_id', 'raw_material_source_id',
            'part_number_id', 'item_code_id'
        ]
    
    def create(self, validated_data):
        product_id = validated_data.pop('product_id', None)
        raw_material_source_id = validated_data.pop('raw_material_source_id', None)
        part_number_id = validated_data.pop('part_number_id', None)
        item_code_id = validated_data.pop('item_code_id', None)
        
        instance = ProductRawMaterial.objects.create(**validated_data)
        
        if product_id:
            instance.product_id = product_id
        if raw_material_source_id:
            instance.raw_material_source_id = raw_material_source_id
        if part_number_id:
            instance.part_number_id = part_number_id
        if item_code_id:
            instance.item_code_id = item_code_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        product_id = validated_data.pop('product_id', None)
        raw_material_source_id = validated_data.pop('raw_material_source_id', None)
        part_number_id = validated_data.pop('part_number_id', None)
        item_code_id = validated_data.pop('item_code_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if product_id is not None:
            instance.product_id = product_id
        if raw_material_source_id is not None:
            instance.raw_material_source_id = raw_material_source_id
        if part_number_id is not None:
            instance.part_number_id = part_number_id
        if item_code_id is not None:
            instance.item_code_id = item_code_id
        
        instance.save()
        return instance


class SecondryWarehouseSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    raw_materials = serializers.SerializerMethodField()
    
    class Meta:
        model = SecondryWarehouse
        fields = [
            'id', 'created_by', 'product_name', 'product_serial_number',
            'manufacturing_start_date', 'manufacturing_end_date', 'test_qc_start_date',
            'test_qc_end_date', 'test_approver', 'qc_responsible', 'product_exit_date',
            'exit_type', 'deliverer', 'receiver', 'finished_price', 'raw_materials'
        ]
    
    def get_raw_materials(self, obj):
        raw_materials = obj.raw_materials.all()
        return SecondryWarehouseRawMaterialSerializer(raw_materials, many=True).data


class SecondryWarehouseRawMaterialSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    secondryWarehouse = SecondryWarehouseSerializer(read_only=True)
    raw_material_source = RawMaterialWarehouseSerializer(read_only=True)
    part_number = ProductPartSerializer(read_only=True)
    item_code = ProductCodeSerializer(read_only=True)
    
    # برای نوشتن
    secondryWarehouse_id = serializers.IntegerField(write_only=True, required=False)
    raw_material_source_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    part_number_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    item_code_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = SecondryWarehouseRawMaterial
        fields = [
            'id', 'created_by', 'secondryWarehouse', 'raw_material_source', 'raw_material_name',
            'part_number', 'item_code', 'serial_number', 'quantity', 'user_who_used',
            'raw_material_entry_date', 'raw_material_price', 'unit', 'secondryWarehouse_id',
            'raw_material_source_id', 'part_number_id', 'item_code_id'
        ]
    
    def create(self, validated_data):
        secondryWarehouse_id = validated_data.pop('secondryWarehouse_id', None)
        raw_material_source_id = validated_data.pop('raw_material_source_id', None)
        part_number_id = validated_data.pop('part_number_id', None)
        item_code_id = validated_data.pop('item_code_id', None)
        
        instance = SecondryWarehouseRawMaterial.objects.create(**validated_data)
        
        if secondryWarehouse_id:
            instance.secondryWarehouse_id = secondryWarehouse_id
        if raw_material_source_id:
            instance.raw_material_source_id = raw_material_source_id
        if part_number_id:
            instance.part_number_id = part_number_id
        if item_code_id:
            instance.item_code_id = item_code_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        secondryWarehouse_id = validated_data.pop('secondryWarehouse_id', None)
        raw_material_source_id = validated_data.pop('raw_material_source_id', None)
        part_number_id = validated_data.pop('part_number_id', None)
        item_code_id = validated_data.pop('item_code_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if secondryWarehouse_id is not None:
            instance.secondryWarehouse_id = secondryWarehouse_id
        if raw_material_source_id is not None:
            instance.raw_material_source_id = raw_material_source_id
        if part_number_id is not None:
            instance.part_number_id = part_number_id
        if item_code_id is not None:
            instance.item_code_id = item_code_id
        
        instance.save()
        return instance


class ProductSecondryProductSerializer(serializers.ModelSerializer):
    product = ProductWarehouseSerializer(read_only=True)
    secondry_product = SecondryWarehouseSerializer(read_only=True)
    
    # برای نوشتن
    product_id = serializers.IntegerField(write_only=True, required=False)
    secondry_product_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProductSecondryProduct
        fields = ['id', 'product', 'secondry_product', 'quantity', 'product_id', 'secondry_product_id']
    
    def create(self, validated_data):
        product_id = validated_data.pop('product_id', None)
        secondry_product_id = validated_data.pop('secondry_product_id', None)
        
        instance = ProductSecondryProduct.objects.create(**validated_data)
        
        if product_id:
            instance.product_id = product_id
        if secondry_product_id:
            instance.secondry_product_id = secondry_product_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        product_id = validated_data.pop('product_id', None)
        secondry_product_id = validated_data.pop('secondry_product_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if product_id is not None:
            instance.product_id = product_id
        if secondry_product_id is not None:
            instance.secondry_product_id = secondry_product_id
        
        instance.save()
        return instance


class ProductDeliverySerializer(serializers.ModelSerializer):
    deliverer = UserSerializer(read_only=True)
    product_items = serializers.SerializerMethodField()
    secondry_items = serializers.SerializerMethodField()
    raw_material_items = serializers.SerializerMethodField()
    
    # برای نوشتن
    deliverer_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProductDelivery
        fields = [
            'id', 'receiver_name', 'user_name', 'delivery_date', 'return_date',
            'deliverer', 'product_items', 'secondry_items', 'raw_material_items', 'deliverer_id'
        ]
    
    def get_product_items(self, obj):
        product_items = obj.product_items.all()
        return ProductDeliveryProductSerializer(product_items, many=True).data
    
    def get_secondry_items(self, obj):
        secondry_items = obj.secondry_items.all()
        return ProductDeliverySecondryProductSerializer(secondry_items, many=True).data
    
    def get_raw_material_items(self, obj):
        raw_material_items = obj.raw_material_items.all()
        return ProductDeliveryRawMaterialSerializer(raw_material_items, many=True).data
    
    def create(self, validated_data):
        deliverer_id = validated_data.pop('deliverer_id', None)
        
        instance = ProductDelivery.objects.create(**validated_data)
        
        if deliverer_id:
            instance.deliverer_id = deliverer_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        deliverer_id = validated_data.pop('deliverer_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if deliverer_id is not None:
            instance.deliverer_id = deliverer_id
        
        instance.save()
        return instance


class ProductDeliveryProductSerializer(serializers.ModelSerializer):
    delivery = ProductDeliverySerializer(read_only=True)
    product = ProductWarehouseSerializer(read_only=True)
    
    # برای نوشتن
    delivery_id = serializers.IntegerField(write_only=True, required=False)
    product_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProductDeliveryProduct
        fields = [
            'id', 'delivery', 'product', 'quantity', 'delivery_date', 'return_date',
            'delivery_id', 'product_id'
        ]
    
    def create(self, validated_data):
        delivery_id = validated_data.pop('delivery_id', None)
        product_id = validated_data.pop('product_id', None)
        
        instance = ProductDeliveryProduct.objects.create(**validated_data)
        
        if delivery_id:
            instance.delivery_id = delivery_id
        if product_id:
            instance.product_id = product_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        delivery_id = validated_data.pop('delivery_id', None)
        product_id = validated_data.pop('product_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if delivery_id is not None:
            instance.delivery_id = delivery_id
        if product_id is not None:
            instance.product_id = product_id
        
        instance.save()
        return instance


class ProductDeliverySecondryProductSerializer(serializers.ModelSerializer):
    delivery = ProductDeliverySerializer(read_only=True)
    secondry_product = SecondryWarehouseSerializer(read_only=True)
    
    # برای نوشتن
    delivery_id = serializers.IntegerField(write_only=True, required=False)
    secondry_product_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProductDeliverySecondryProduct
        fields = [
            'id', 'delivery', 'secondry_product', 'quantity', 'delivery_date', 'return_date',
            'delivery_id', 'secondry_product_id'
        ]
    
    def create(self, validated_data):
        delivery_id = validated_data.pop('delivery_id', None)
        secondry_product_id = validated_data.pop('secondry_product_id', None)
        
        instance = ProductDeliverySecondryProduct.objects.create(**validated_data)
        
        if delivery_id:
            instance.delivery_id = delivery_id
        if secondry_product_id:
            instance.secondry_product_id = secondry_product_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        delivery_id = validated_data.pop('delivery_id', None)
        secondry_product_id = validated_data.pop('secondry_product_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if delivery_id is not None:
            instance.delivery_id = delivery_id
        if secondry_product_id is not None:
            instance.secondry_product_id = secondry_product_id
        
        instance.save()
        return instance


class ProductDeliveryRawMaterialSerializer(serializers.ModelSerializer):
    delivery = ProductDeliverySerializer(read_only=True)
    raw_material = RawMaterialWarehouseSerializer(read_only=True)
    part_number = ProductPartSerializer(read_only=True)
    item_code = ProductCodeSerializer(read_only=True)
    
    # برای نوشتن
    delivery_id = serializers.IntegerField(write_only=True, required=False)
    raw_material_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    part_number_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    item_code_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProductDeliveryRawMaterial
        fields = [
            'id', 'delivery', 'raw_material', 'quantity', 'delivery_date', 'return_date',
            'raw_material_name', 'part_number', 'item_code', 'serial_number', 'user_who_used',
            'raw_material_entry_date', 'raw_material_price', 'unit', 'delivery_id', 'raw_material_id',
            'part_number_id', 'item_code_id'
        ]
    
    def create(self, validated_data):
        delivery_id = validated_data.pop('delivery_id', None)
        raw_material_id = validated_data.pop('raw_material_id', None)
        part_number_id = validated_data.pop('part_number_id', None)
        item_code_id = validated_data.pop('item_code_id', None)
        
        instance = ProductDeliveryRawMaterial.objects.create(**validated_data)
        
        if delivery_id:
            instance.delivery_id = delivery_id
        if raw_material_id:
            instance.raw_material_id = raw_material_id
        if part_number_id:
            instance.part_number_id = part_number_id
        if item_code_id:
            instance.item_code_id = item_code_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        delivery_id = validated_data.pop('delivery_id', None)
        raw_material_id = validated_data.pop('raw_material_id', None)
        part_number_id = validated_data.pop('part_number_id', None)
        item_code_id = validated_data.pop('item_code_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if delivery_id is not None:
            instance.delivery_id = delivery_id
        if raw_material_id is not None:
            instance.raw_material_id = raw_material_id
        if part_number_id is not None:
            instance.part_number_id = part_number_id
        if item_code_id is not None:
            instance.item_code_id = item_code_id
        
        instance.save()
        return instance


class ExternalProductDeliverySerializer(serializers.ModelSerializer):
    deliverer = UserSerializer(read_only=True)
    product_items = serializers.SerializerMethodField()
    secondry_items = serializers.SerializerMethodField()
    raw_material_items = serializers.SerializerMethodField()
    
    # برای نوشتن
    deliverer_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ExternalProductDelivery
        fields = [
            'id', 'receiver_name', 'delivery_date', 'return_date', 'reference_letter',
            'deliverer', 'product_items', 'secondry_items', 'raw_material_items', 'deliverer_id'
        ]
    
    def get_product_items(self, obj):
        product_items = obj.product_items.all()
        return ExternalProductDeliveryProductSerializer(product_items, many=True).data
    
    def get_secondry_items(self, obj):
        secondry_items = obj.secondry_items.all()
        return ExternalProductDeliverySecondryProductSerializer(secondry_items, many=True).data
    
    def get_raw_material_items(self, obj):
        raw_material_items = obj.raw_material_items.all()
        return ExternalProductDeliveryRawMaterialSerializer(raw_material_items, many=True).data
    
    def create(self, validated_data):
        deliverer_id = validated_data.pop('deliverer_id', None)
        
        instance = ExternalProductDelivery.objects.create(**validated_data)
        
        if deliverer_id:
            instance.deliverer_id = deliverer_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        deliverer_id = validated_data.pop('deliverer_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if deliverer_id is not None:
            instance.deliverer_id = deliverer_id
        
        instance.save()
        return instance


class ExternalProductDeliveryProductSerializer(serializers.ModelSerializer):
    delivery = ExternalProductDeliverySerializer(read_only=True)
    product = ProductWarehouseSerializer(read_only=True)
    
    # برای نوشتن
    delivery_id = serializers.IntegerField(write_only=True, required=False)
    product_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ExternalProductDeliveryProduct
        fields = [
            'id', 'delivery', 'product', 'quantity', 'delivery_date', 'return_date',
            'delivery_id', 'product_id'
        ]
    
    def create(self, validated_data):
        delivery_id = validated_data.pop('delivery_id', None)
        product_id = validated_data.pop('product_id', None)
        
        instance = ExternalProductDeliveryProduct.objects.create(**validated_data)
        
        if delivery_id:
            instance.delivery_id = delivery_id
        if product_id:
            instance.product_id = product_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        delivery_id = validated_data.pop('delivery_id', None)
        product_id = validated_data.pop('product_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if delivery_id is not None:
            instance.delivery_id = delivery_id
        if product_id is not None:
            instance.product_id = product_id
        
        instance.save()
        return instance


class ExternalProductDeliverySecondryProductSerializer(serializers.ModelSerializer):
    delivery = ExternalProductDeliverySerializer(read_only=True)
    secondry_product = SecondryWarehouseSerializer(read_only=True)
    
    # برای نوشتن
    delivery_id = serializers.IntegerField(write_only=True, required=False)
    secondry_product_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ExternalProductDeliverySecondryProduct
        fields = [
            'id', 'delivery', 'secondry_product', 'quantity', 'delivery_date', 'return_date',
            'delivery_id', 'secondry_product_id'
        ]
    
    def create(self, validated_data):
        delivery_id = validated_data.pop('delivery_id', None)
        secondry_product_id = validated_data.pop('secondry_product_id', None)
        
        instance = ExternalProductDeliverySecondryProduct.objects.create(**validated_data)
        
        if delivery_id:
            instance.delivery_id = delivery_id
        if secondry_product_id:
            instance.secondry_product_id = secondry_product_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        delivery_id = validated_data.pop('delivery_id', None)
        secondry_product_id = validated_data.pop('secondry_product_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if delivery_id is not None:
            instance.delivery_id = delivery_id
        if secondry_product_id is not None:
            instance.secondry_product_id = secondry_product_id
        
        instance.save()
        return instance


class ExternalProductDeliveryRawMaterialSerializer(serializers.ModelSerializer):
    delivery = ExternalProductDeliverySerializer(read_only=True)
    raw_material = RawMaterialWarehouseSerializer(read_only=True)
    
    # برای نوشتن
    delivery_id = serializers.IntegerField(write_only=True, required=False)
    raw_material_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ExternalProductDeliveryRawMaterial
        fields = [
            'id', 'delivery', 'raw_material', 'quantity', 'delivery_date', 'return_date',
            'delivery_id', 'raw_material_id'
        ]
    
    def create(self, validated_data):
        delivery_id = validated_data.pop('delivery_id', None)
        raw_material_id = validated_data.pop('raw_material_id', None)
        
        instance = ExternalProductDeliveryRawMaterial.objects.create(**validated_data)
        
        if delivery_id:
            instance.delivery_id = delivery_id
        if raw_material_id:
            instance.raw_material_id = raw_material_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        delivery_id = validated_data.pop('delivery_id', None)
        raw_material_id = validated_data.pop('raw_material_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if delivery_id is not None:
            instance.delivery_id = delivery_id
        if raw_material_id is not None:
            instance.raw_material_id = raw_material_id
        
        instance.save()
        return instance


class ReturnedFromCustomerSerializer(serializers.ModelSerializer):
    received_by = UserSerializer(read_only=True)
    
    # برای نوشتن
    received_by_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ReturnedFromCustomer
        fields = [
            'id', 'customer_name', 'product_name', 'product_serial_number',
            'product_part_number', 'product_item_code', 'return_reason', 'return_date',
            'received_by', 'received_by_id'
        ]
    
    def create(self, validated_data):
        received_by_id = validated_data.pop('received_by_id', None)
        
        instance = ReturnedFromCustomer.objects.create(**validated_data)
        
        if received_by_id:
            instance.received_by_id = received_by_id
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        received_by_id = validated_data.pop('received_by_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if received_by_id is not None:
            instance.received_by_id = received_by_id
        
        instance.save()
        return instance


class BorrowedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedProduct
        fields = [
            'id', 'product_name', 'serial_number', 'giver_company',
            'receiver_person', 'delivery_date', 'return_date'
        ]


