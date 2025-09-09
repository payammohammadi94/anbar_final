# راهنمای ورود و استفاده از API

## مشکل HTTP 401 Unauthorized حل شد! ✅

### مراحل ورود به سیستم:

#### 1. ایجاد کاربر ادمین (اگر قبلاً ایجاد نکرده‌اید):
```bash
python manage.py createsuperuser
```
- نام کاربری: `admin` (یا هر نام دلخواه)
- ایمیل: `admin@example.com`
- رمز عبور: یک رمز قوی انتخاب کنید

#### 2. اجرای سرور:
```bash
python manage.py runserver
```

#### 3. ورود به سیستم:
- به آدرس `http://127.0.0.1:8000/` بروید
- صفحه لاگین زیبا و فارسی نمایش داده می‌شود
- نام کاربری و رمز عبور خود را وارد کنید
- روی دکمه "ورود" کلیک کنید

#### 4. دریافت توکن:
- پس از ورود موفق، توکن JWT نمایش داده می‌شود
- توکن در localStorage مرورگر ذخیره می‌شود
- این توکن برای دسترسی به API استفاده می‌شود

### استفاده از API:

#### 1. دریافت توکن از طریق API:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

#### 2. استفاده از توکن در درخواست‌ها:
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://127.0.0.1:8000/api/categories/
```

#### 3. در JavaScript:
```javascript
fetch('/api/categories/', {
    headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
    }
})
.then(response => response.json())
.then(data => console.log(data));
```

### Endpoints احراز هویت:

- **POST** `/api/auth/login/` - دریافت توکن دسترسی
- **POST** `/api/auth/refresh/` - تمدید توکن

### مثال کامل لاگین:

```python
import requests

# لاگین
login_data = {
    "username": "admin",
    "password": "your_password"
}

response = requests.post('http://127.0.0.1:8000/api/auth/login/', json=login_data)
tokens = response.json()

access_token = tokens['access']
refresh_token = tokens['refresh']

# استفاده از توکن
headers = {
    'Authorization': f'Bearer {access_token}'
}

# درخواست به API
api_response = requests.get('http://127.0.0.1:8000/api/categories/', headers=headers)
data = api_response.json()
print(data)
```

### ویژگی‌های صفحه لاگین:

- ✅ طراحی زیبا و فارسی
- ✅ ذخیره خودکار توکن در localStorage
- ✅ نمایش توکن پس از ورود موفق
- ✅ پیام‌های خطا و موفقیت
- ✅ لینک‌های مستقیم به API و پنل ادمین
- ✅ بررسی وضعیت ورود قبلی

### نکات مهم:

1. **توکن منقضی می‌شود**: توکن دسترسی پس از 1 روز منقضی می‌شود
2. **تجدید توکن**: از `/api/auth/refresh/` برای تمدید توکن استفاده کنید
3. **امنیت**: توکن را در جای امن نگهداری کنید
4. **HTTPS**: در production از HTTPS استفاده کنید

### تست API:

پس از ورود، می‌توانید این endpoints را تست کنید:

- `GET /api/categories/` - لیست دسته‌بندی‌ها
- `GET /api/quarantine-warehouse/` - انبار قرنطینه
- `GET /api/raw-material-warehouse/` - انبار مواد اولیه
- `GET /api/product-warehouse/` - انبار محصولات

### مشکل حل شد! 🎉

حالا می‌توانید:
1. به `http://127.0.0.1:8000/` بروید
2. وارد شوید
3. توکن دریافت کنید
4. از API استفاده کنید


