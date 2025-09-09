# راهنمای Export به Excel

## 🎯 قابلیت‌های اضافه شده

حالا می‌توانید تمام داده‌های API را به فایل Excel export کنید!

## 📊 Endpoints موجود

### 1. **Export انبارهای جداگانه**

#### دسته‌بندی‌ها:
```
GET /api/categories/export_excel/
```

#### انبار قرنطینه:
```
GET /api/quarantine-warehouse/export_excel/
```

#### انبار مواد اولیه:
```
GET /api/raw-material-warehouse/export_excel/
```

#### انبار محصولات:
```
GET /api/product-warehouse/export_excel/
```

#### انبار ثانویه:
```
GET /api/secondry-warehouse/export_excel/
```

### 2. **Export تمام انبارها در یک فایل**
```
GET /api/export/excel/
```

## 🔧 نحوه استفاده

### 1. **از طریق مرورگر:**
- به آدرس endpoint مورد نظر بروید
- فایل Excel به طور خودکار دانلود می‌شود

### 2. **از طریق cURL:**
```bash
# Export انبار قرنطینه
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/quarantine-warehouse/export_excel/ \
  --output quarantine_warehouse.xlsx

# Export تمام انبارها
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/export/excel/ \
  --output all_warehouses.xlsx
```

### 3. **از طریق JavaScript:**
```javascript
// Export انبار قرنطینه
fetch('/api/quarantine-warehouse/export_excel/', {
    headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
    }
})
.then(response => response.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'quarantine_warehouse.xlsx';
    a.click();
});

// Export تمام انبارها
fetch('/api/export/excel/', {
    headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
    }
})
.then(response => response.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'all_warehouses.xlsx';
    a.click();
});
```

### 4. **از طریق Python:**
```python
import requests

# Export انبار قرنطینه
response = requests.get(
    'http://127.0.0.1:8000/api/quarantine-warehouse/export_excel/',
    headers={'Authorization': 'Bearer YOUR_TOKEN'}
)

with open('quarantine_warehouse.xlsx', 'wb') as f:
    f.write(response.content)

# Export تمام انبارها
response = requests.get(
    'http://127.0.0.1:8000/api/export/excel/',
    headers={'Authorization': 'Bearer YOUR_TOKEN'}
)

with open('all_warehouses.xlsx', 'wb') as f:
    f.write(response.content)
```

## 📋 ویژگی‌های فایل Excel

### 1. **فایل‌های جداگانه:**
- **نام فایل**: بر اساس نوع انبار
- **Sheet**: یک sheet با نام "Data"
- **ستون‌ها**: تمام فیلدهای مدل
- **روابط**: فیلدهای مربوطه به صورت متن

### 2. **فایل کلی (تمام انبارها):**
- **نام فایل**: "all_warehouses.xlsx"
- **Sheet ها**:
  - Categories
  - Quarantine_Warehouse
  - Raw_Material_Warehouse
  - Product_Warehouse
  - Secondry_Warehouse

### 3. **بهینه‌سازی‌ها:**
- **عرض ستون‌ها**: خودکار تنظیم می‌شود
- **حداکثر عرض**: 50 کاراکتر
- **فیلترها**: اعمال فیلترهای API
- **Pagination**: تمام داده‌ها export می‌شوند

## 🎨 مثال‌های عملی

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

## 🚀 تست سریع

1. **وارد شوید:**
   ```
   http://127.0.0.1:8000/api/login/
   ```

2. **Export کنید:**
   ```
   http://127.0.0.1:8000/api/categories/export_excel/
   ```

3. **فایل Excel دانلود می‌شود!** ✅

## 📈 آمار Export

- **تعداد endpoints**: 5+ endpoint برای export
- **فرمت خروجی**: Excel (.xlsx)
- **پشتیبانی از فیلتر**: ✅
- **پشتیبانی از جستجو**: ✅
- **پشتیبانی از pagination**: ✅
- **Export کلی**: ✅

حالا می‌توانید تمام داده‌های انبار را به Excel export کنید! 🎉
