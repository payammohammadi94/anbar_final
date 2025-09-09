# راهنمای کامل Export به Excel

## 🎯 تمام Endpoints Export Excel

حالا تمام کلاس‌های مدل دارای قابلیت export به Excel هستند!

## 📊 لیست کامل Endpoints

### 1. **All Warehouses** 🏭
- **Endpoint**: `/api/export/excel/`
- **فایل**: `all_warehouses.xlsx`
- **توضیح**: تمام انبارها در یک فایل با sheet های جداگانه

### 2. **Categories** 🏷️
- **Endpoint**: `/api/categories/export_excel/`
- **فایل**: `categories.xlsx`
- **توضیح**: دسته‌بندی‌ها

### 3. **Product Parts** 🧩
- **Endpoint**: `/api/product-parts/export_excel/`
- **فایل**: `product_parts.xlsx`
- **توضیح**: قطعات محصول

### 4. **Product Codes** 📊
- **Endpoint**: `/api/product-codes/export_excel/`
- **فایل**: `product_codes.xlsx`
- **توضیح**: کدهای محصول

### 5. **Quarantine Warehouse** 🛡️
- **Endpoint**: `/api/quarantine-warehouse/export_excel/`
- **فایل**: `quarantine_warehouse.xlsx`
- **توضیح**: انبار قرنطینه

### 6. **Raw Material Warehouse** 📦
- **Endpoint**: `/api/raw-material-warehouse/export_excel/`
- **فایل**: `raw_material_warehouse.xlsx`
- **توضیح**: انبار مواد اولیه

### 7. **Product Warehouse** 🧊
- **Endpoint**: `/api/product-warehouse/export_excel/`
- **فایل**: `product_warehouse.xlsx`
- **توضیح**: انبار محصولات

### 8. **Returned Products** ↩️
- **Endpoint**: `/api/returned-products/export_excel/`
- **فایل**: `returned_products.xlsx`
- **توضیح**: محصولات برگشتی

### 9. **Secondary Warehouse** 🔄
- **Endpoint**: `/api/secondry-warehouse/export_excel/`
- **فایل**: `secondry_warehouse.xlsx`
- **توضیح**: انبار ثانویه

### 10. **Product Delivery** 🚚
- **Endpoint**: `/api/product-delivery/export_excel/`
- **فایل**: `product_delivery.xlsx`
- **توضیح**: تحویل محصولات

### 11. **External Product Delivery** 🚛
- **Endpoint**: `/api/external-product-delivery/export_excel/`
- **فایل**: `external_product_delivery.xlsx`
- **توضیح**: تحویل محصولات خارجی

### 12. **Returned From Customer** 👤
- **Endpoint**: `/api/returned-from-customer/export_excel/`
- **فایل**: `returned_from_customer.xlsx`
- **توضیح**: محصولات برگشتی از مشتری

### 13. **Borrowed Products** 🤝
- **Endpoint**: `/api/borrowed-products/export_excel/`
- **فایل**: `borrowed_products.xlsx`
- **توضیح**: محصولات قرضی

## 🎨 ویژگی‌های دکمه Excel

### 1. **طراحی جدید:**
- **Grid Layout**: لینک‌ها در دو ستون
- **Scroll**: اگر لینک‌ها زیاد باشند، scroll می‌شود
- **آیکون‌های مناسب**: هر لینک آیکون مخصوص خود را دارد

### 2. **لینک‌های موجود:**
- **All Warehouses** - تمام انبارها
- **Categories** - دسته‌بندی‌ها
- **Product Parts** - قطعات محصول
- **Product Codes** - کدهای محصول
- **Quarantine Warehouse** - انبار قرنطینه
- **Raw Material Warehouse** - انبار مواد اولیه
- **Product Warehouse** - انبار محصولات
- **Returned Products** - محصولات برگشتی
- **Secondary Warehouse** - انبار ثانویه
- **Product Delivery** - تحویل محصولات
- **External Product Delivery** - تحویل محصولات خارجی
- **Returned From Customer** - محصولات برگشتی از مشتری
- **Borrowed Products** - محصولات قرضی

## 🚀 نحوه استفاده

### 1. **از طریق دکمه Excel:**
1. روی دکمه "Excel Export" کلیک کنید
2. منو باز می‌شود
3. روی لینک مورد نظر کلیک کنید
4. فایل Excel دانلود می‌شود

### 2. **از طریق URL مستقیم:**
```
http://127.0.0.1:8000/api/categories/export_excel/
http://127.0.0.1:8000/api/product-parts/export_excel/
http://127.0.0.1:8000/api/quarantine-warehouse/export_excel/
```

### 3. **از طریق cURL:**
```bash
# Export دسته‌بندی‌ها
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/categories/export_excel/ \
  --output categories.xlsx

# Export انبار قرنطینه
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/quarantine-warehouse/export_excel/ \
  --output quarantine_warehouse.xlsx
```

## 🔧 تست کردن

### 1. **تست دکمه Excel:**
1. به `http://127.0.0.1:8000/` بروید
2. روی دکمه "Excel Export" کلیک کنید
3. منو باز می‌شود
4. روی هر لینک کلیک کنید
5. فایل Excel دانلود می‌شود

### 2. **تست endpoints:**
```bash
# تست endpoint دسته‌بندی‌ها
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/categories/export_excel/

# تست endpoint انبار قرنطینه
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/quarantine-warehouse/export_excel/
```

## 📋 ویژگی‌های فایل Excel

### 1. **فایل‌های جداگانه:**
- **نام فایل**: بر اساس نوع مدل
- **Sheet**: یک sheet با نام "Data"
- **ستون‌ها**: تمام فیلدهای مدل
- **روابط**: فیلدهای مربوطه به صورت متن

### 2. **فایل کلی (All Warehouses):**
- **نام فایل**: "all_warehouses.xlsx"
- **Sheet ها**:
  - Categories
  - ProductParts
  - ProductCodes
  - Quarantine_Warehouse
  - Raw_Material_Warehouse
  - Product_Warehouse
  - Returned_Products
  - Secondry_Warehouse
  - Product_Delivery
  - External_Product_Delivery
  - Returned_From_Customer
  - Borrowed_Products

### 3. **بهینه‌سازی‌ها:**
- **عرض ستون‌ها**: خودکار تنظیم می‌شود
- **حداکثر عرض**: 50 کاراکتر
- **فیلترها**: اعمال فیلترهای API
- **Pagination**: تمام داده‌ها export می‌شوند

## 🎯 مثال‌های عملی

### Export با فیلتر:
```
# Export انبار قرنطینه با وضعیت خاص
GET /api/quarantine-warehouse/export_excel/?status=waiting_test

# Export انبار مواد اولیه با موجودی کم
GET /api/raw-material-warehouse/export_excel/?quantity__lte=10

# Export دسته‌بندی‌های اصلی
GET /api/categories/export_excel/?is_sub=false
```

### Export با جستجو:
```
# Export محصولات با نام خاص
GET /api/product-warehouse/export_excel/?search=موبایل

# Export انبار قرنطینه با تامین کننده خاص
GET /api/quarantine-warehouse/export_excel/?search=شرکت الف
```

## 🔍 عیب‌یابی

### اگر فایل Excel دانلود نمی‌شود:

1. **بررسی احراز هویت:**
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://127.0.0.1:8000/api/categories/export_excel/
   ```

2. **بررسی خطاها:**
   - Console مرورگر را بررسی کنید
   - Network tab را چک کنید
   - Response status code را بررسی کنید

3. **بررسی کتابخانه‌ها:**
   ```bash
   pip install openpyxl xlsxwriter pandas
   ```

## 💡 نکات مهم

1. **حجم داده**: برای داده‌های زیاد، ممکن است export زمان‌بر باشد
2. **احراز هویت**: تمام endpoints نیاز به احراز هویت دارند
3. **فیلترها**: می‌توانید از تمام فیلترهای API استفاده کنید
4. **فرمت فایل**: فایل‌ها در فرمت .xlsx هستند

## 🎉 نتیجه

حالا می‌توانید تمام داده‌های انبار را به Excel export کنید!

**فقط کافی است:**
1. روی دکمه "Excel Export" کلیک کنید
2. لینک مورد نظر را انتخاب کنید
3. فایل Excel دانلود می‌شود! ✅

**تعداد کل endpoints**: 13 endpoint برای export
**فرمت خروجی**: Excel (.xlsx)
**پشتیبانی از فیلتر**: ✅
**پشتیبانی از جستجو**: ✅
**Export کلی**: ✅
