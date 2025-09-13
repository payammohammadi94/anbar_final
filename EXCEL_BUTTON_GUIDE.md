# راهنمای دکمه Excel Export

## 🎯 ویژگی‌های اضافه شده

حالا در صفحه اصلی یک دکمه **Excel Export** اضافه شده که تمام لینک‌های export را در خود دارد!

## 🎨 طراحی دکمه

### 1. **دکمه اصلی:**
- **رنگ**: سبز (Gradient)
- **آیکون**: 📊 Excel
- **متن**: "Excel Export"
- **موقعیت**: زیر دکمه‌های Admin Panel و API Panel

### 2. **Dropdown منو:**
- **موقعیت**: زیر دکمه Excel
- **طراحی**: کارت سفید با سایه
- **انیمیشن**: نمایش/مخفی شدن نرم

## 📋 لینک‌های موجود در Dropdown

### 1. **All Warehouses** 🏭
- **لینک**: `/api/export/excel/`
- **فایل**: `all_warehouses.xlsx`
- **توضیح**: تمام انبارها در یک فایل

### 2. **Categories** 🏷️
- **لینک**: `/api/categories/export_excel/`
- **فایل**: `categories.xlsx`
- **توضیح**: دسته‌بندی‌ها

### 3. **Quarantine Warehouse** 🛡️
- **لینک**: `/api/quarantine-warehouse/export_excel/`
- **فایل**: `quarantine_warehouse.xlsx`
- **توضیح**: انبار قرنطینه

### 4. **Raw Material Warehouse** 📦
- **لینک**: `/api/raw-material-warehouse/export_excel/`
- **فایل**: `raw_material_warehouse.xlsx`
- **توضیح**: انبار مواد اولیه

### 5. **Product Warehouse** 🧊
- **لینک**: `/api/product-warehouse/export_excel/`
- **فایل**: `product_warehouse.xlsx`
- **توضیح**: انبار محصولات

### 6. **Secondary Warehouse** 🔄
- **لینک**: `/api/secondry-warehouse/export_excel/`
- **فایل**: `secondry_warehouse.xlsx`
- **توضیح**: انبار ثانویه

## 🚀 نحوه استفاده

### 1. **باز کردن Dropdown:**
- روی دکمه "Excel Export" کلیک کنید
- منو باز می‌شود

### 2. **بستن Dropdown:**
- روی دکمه "Excel Export" دوباره کلیک کنید
- یا روی جای دیگری از صفحه کلیک کنید

### 3. **دانلود فایل:**
- روی لینک مورد نظر کلیک کنید
- فایل Excel به طور خودکار دانلود می‌شود

## ⚡ ویژگی‌های JavaScript

### 1. **Loading Animation:**
- هنگام دانلود، آیکون spinner نمایش داده می‌شود
- متن به "Downloading..." تغییر می‌کند

### 2. **Success/Error Messages:**
- پیام موفقیت: "File downloaded successfully!"
- پیام خطا: "Error downloading file. Please try again."

### 3. **Token Authentication:**
- اگر token در localStorage موجود باشد، استفاده می‌شود
- در غیر این صورت، درخواست بدون احراز هویت ارسال می‌شود

### 4. **Auto Download:**
- فایل به طور خودکار دانلود می‌شود
- نیازی به کلیک اضافی نیست

## 🎨 CSS Styling

### 1. **دکمه Excel:**
```css
.btn-excel {
    background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
    color: white;
}
```

### 2. **Dropdown:**
```css
.excel-content {
    position: absolute;
    background-color: white;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    border-radius: 8px;
}
```

### 3. **لینک‌ها:**
```css
.excel-link {
    background: #f8f9fa;
    color: #333;
    border-radius: 5px;
}
```

## 🔧 تست کردن

### 1. **باز کردن صفحه:**
```
http://127.0.0.1:8000/
```

### 2. **کلیک روی Excel Export:**
- دکمه سبز را کلیک کنید
- منو باز می‌شود

### 3. **انتخاب لینک:**
- روی هر لینک کلیک کنید
- فایل Excel دانلود می‌شود

## 📱 Responsive Design

### 1. **موبایل:**
- دکمه‌ها در یک ستون قرار می‌گیرند
- Dropdown در وسط صفحه نمایش داده می‌شود

### 2. **دسکتاپ:**
- دکمه‌ها در یک ردیف قرار می‌گیرند
- Dropdown زیر دکمه Excel نمایش داده می‌شود

## 🎯 مزایای این روش

### 1. **راحتی استفاده:**
- تمام لینک‌ها در یک مکان
- نیازی به یادآوری URL ها نیست

### 2. **UI/UX بهتر:**
- طراحی زیبا و مدرن
- انیمیشن‌های نرم

### 3. **احراز هویت خودکار:**
- استفاده از token موجود
- نیازی به ورود مجدد نیست

### 4. **پیام‌های کاربردی:**
- اطلاع‌رسانی موفقیت/خطا
- نمایش وضعیت دانلود

## 🚨 نکات مهم

### 1. **احراز هویت:**
- برای استفاده از API ها، ابتدا وارد شوید
- Token در localStorage ذخیره می‌شود

### 2. **مرورگر:**
- از مرورگرهای مدرن استفاده کنید
- JavaScript باید فعال باشد

### 3. **فایل‌ها:**
- فایل‌ها در پوشه Downloads ذخیره می‌شوند
- نام فایل‌ها به صورت خودکار تنظیم می‌شود

## 🎉 نتیجه

حالا می‌توانید به راحتی تمام داده‌های انبار را به Excel export کنید! 

**فقط کافی است:**
1. روی دکمه "Excel Export" کلیک کنید
2. لینک مورد نظر را انتخاب کنید
3. فایل Excel دانلود می‌شود! ✅

