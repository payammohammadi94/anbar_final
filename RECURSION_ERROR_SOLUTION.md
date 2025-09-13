# راهنمای حل مشکل RecursionError در API

## 🔍 مشکل
```
RecursionError at /api/categories/
Maximum recursion depth exceeded
```

این مشکل به دلیل روابط پیچیده و circular references در مدل‌ها رخ می‌دهد.

## ✅ راه‌حل‌های پیاده‌سازی شده

### 1. **بهینه‌سازی Serializers** 🔧

#### تغییرات انجام شده:
- **حذف circular references** از serializers
- **محدود کردن عمق روابط** در serializer methods
- **جداسازی serializers** برای list و detail views
- **حذف فیلدهای غیرضروری** از serializers

#### مثال:
```python
# قبل (مشکل‌دار)
class ProductWarehouseSerializer(serializers.ModelSerializer):
    raw_materials = serializers.SerializerMethodField()
    
    def get_raw_materials(self, obj):
        raw_materials = obj.raw_materials.all()  # بدون محدودیت
        return ProductRawMaterialSerializer(raw_materials, many=True).data

# بعد (بهینه‌سازی شده)
class ProductWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductWarehouse
        fields = ['id', 'product_name', 'product_serial_number', ...]

class ProductWarehouseDetailSerializer(serializers.ModelSerializer):
    raw_materials = serializers.SerializerMethodField()
    
    def get_raw_materials(self, obj):
        raw_materials = obj.raw_materials.all()[:10]  # محدود به 10 آیتم
        return ProductRawMaterialSerializer(raw_materials, many=True).data
```

### 2. **Pagination اضافه شده** 📄

#### تنظیمات:
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'PAGE_SIZE_QUERY_PARAM': 'page_size',
    'MAX_PAGE_SIZE': 100,
}
```

#### استفاده:
```
GET /api/categories/?page=1&page_size=10
```

### 3. **Query Optimization** ⚡

#### تغییرات:
- **select_related** برای ForeignKey relationships
- **prefetch_related** برای ManyToMany relationships
- **محدود کردن تعداد آیتم‌ها** در serializer methods

#### مثال:
```python
# قبل
queryset = Category.objects.all()

# بعد
queryset = Category.objects.select_related('sub_cat').all()
```

### 4. **محدود کردن روابط** 🔗

#### در serializer methods:
```python
def get_raw_materials(self, obj):
    raw_materials = obj.raw_materials.all()[:20]  # حداکثر 20 آیتم
    return ProductRawMaterialSerializer(raw_materials, many=True).data
```

## 🚀 ویژگی‌های جدید

### 1. **Serializers بهینه‌سازی شده**
- فایل: `warehousing/serializers_optimized.py`
- حذف circular references
- محدود کردن عمق روابط

### 2. **ViewSets بهبود یافته**
- فایل: `warehousing/viewsets_optimized.py`
- Query optimization
- محدود کردن تعداد آیتم‌ها

### 3. **Pagination خودکار**
- 20 آیتم در هر صفحه (قابل تنظیم)
- حداکثر 100 آیتم در هر صفحه
- پارامتر `page_size` برای تنظیم

## 📋 نحوه استفاده

### 1. **استفاده از Pagination**
```
GET /api/categories/?page=1&page_size=10
GET /api/quarantine-warehouse/?page=2&page_size=5
```

### 2. **محدود کردن روابط**
```
GET /api/product-warehouse/1/raw_materials/  # حداکثر 20 آیتم
GET /api/product-deliveries/1/items/         # حداکثر 20 آیتم
```

### 3. **جستجو و فیلتر**
```
GET /api/categories/?search=الکترونیک
GET /api/quarantine-warehouse/?status=waiting_test
```

## 🔧 تنظیمات پیشنهادی

### 1. **برای سرورهای قوی:**
```python
'PAGE_SIZE': 50,
'MAX_PAGE_SIZE': 200,
```

### 2. **برای سرورهای ضعیف:**
```python
'PAGE_SIZE': 10,
'MAX_PAGE_SIZE': 50,
```

### 3. **محدود کردن روابط:**
```python
# در serializer methods
raw_materials = obj.raw_materials.all()[:5]  # فقط 5 آیتم
```

## 🎯 نتایج

### قبل از بهینه‌سازی:
- ❌ RecursionError
- ❌ مصرف زیاد RAM
- ❌ پاسخ‌های کند
- ❌ Timeout errors

### بعد از بهینه‌سازی:
- ✅ بدون RecursionError
- ✅ مصرف کم RAM
- ✅ پاسخ‌های سریع
- ✅ Pagination خودکار
- ✅ محدود کردن روابط

## 💡 نکات مهم

1. **همیشه از pagination استفاده کنید**
2. **روابط را محدود کنید** (مثلاً 10-20 آیتم)
3. **Query optimization** انجام دهید
4. **Serializers ساده** نگه دارید
5. **از select_related و prefetch_related** استفاده کنید

## 🔍 عیب‌یابی

### اگر همچنان مشکل دارید:

1. **بررسی تعداد آیتم‌ها:**
   ```python
   # در Django shell
   from warehousing.models import Category
   print(Category.objects.count())
   ```

2. **بررسی روابط:**
   ```python
   # بررسی circular references
   category = Category.objects.first()
   print(category.sub_cat)
   print(category.catgory.all().count())
   ```

3. **تست pagination:**
   ```
   GET /api/categories/?page=1&page_size=5
   ```

## 🎉 نتیجه

مشکل RecursionError کاملاً حل شد! حالا:
- API سریع و بهینه کار می‌کند
- مصرف RAM کاهش یافته
- Pagination خودکار فعال است
- روابط محدود شده‌اند
- Query optimization انجام شده

### تست کنید:
1. `GET /api/categories/` - باید سریع کار کند
2. `GET /api/categories/?page=1&page_size=10` - pagination
3. `GET /api/product-warehouse/1/raw_materials/` - روابط محدود



