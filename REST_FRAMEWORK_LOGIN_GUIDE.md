# راهنمای حل مشکل HTTP 401 در Django REST Framework

## 🎯 مشکل
در صفحه Django REST framework (Browsable API) خطای HTTP 401 دریافت می‌کنید:
```
HTTP 401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
```

## ✅ راه‌حل‌های ارائه شده

### 1. **Session Authentication** (آسان‌ترین راه)

#### مراحل:
1. به `http://127.0.0.1:8000/api/login/` بروید
2. با نام کاربری و رمز عبور ادمین وارد شوید
3. به طور خودکار به صفحه API منتقل می‌شوید
4. حالا می‌توانید تمام endpoints را مشاهده و تست کنید

### 2. **JWT Token Authentication**

#### دریافت توکن:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### استفاده در REST framework:
1. توکن را کپی کنید
2. در Developer Tools مرورگر، Console را باز کنید
3. این کد را اجرا کنید:
```javascript
localStorage.setItem('jwt_token', 'YOUR_TOKEN_HERE');
location.reload();
```

### 3. **Basic Authentication**

در REST framework:
1. روی دکمه "Log in" کلیک کنید
2. نام کاربری و رمز عبور را وارد کنید
3. یا از Basic Authentication استفاده کنید

## 🔧 تنظیمات انجام شده

### 1. **Authentication Classes اضافه شده:**
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'warehousing.authentication.SessionOrJWTAuthentication',
    ],
    # ...
}
```

### 2. **صفحه لاگین مخصوص API:**
- آدرس: `http://127.0.0.1:8000/api/login/`
- طراحی زیبا و فارسی
- راهنمای کامل احراز هویت

### 3. **Custom Authentication:**
- پشتیبانی از JWT از localStorage
- ترکیب Session و JWT authentication

## 🚀 مراحل تست

### روش 1: Session Authentication
1. `python manage.py runserver`
2. به `http://127.0.0.1:8000/api/login/` بروید
3. وارد شوید
4. به `http://127.0.0.1:8000/api/` بروید
5. حالا می‌توانید API ها را مشاهده کنید

### روش 2: JWT Token
1. به `http://127.0.0.1:8000/` بروید
2. وارد شوید و توکن دریافت کنید
3. توکن را در localStorage ذخیره کنید
4. به `http://127.0.0.1:8000/api/` بروید

### روش 3: Admin Login
1. به `http://127.0.0.1:8000/admin/` بروید
2. وارد شوید
3. به `http://127.0.0.1:8000/api/` بروید

## 📋 چک‌لیست

- [ ] کاربر ادمین ایجاد شده است
- [ ] سرور Django اجرا شده است
- [ ] یکی از روش‌های احراز هویت انجام شده است
- [ ] در REST framework لاگین شده‌اید
- [ ] می‌توانید endpoints را مشاهده کنید

## 🔍 عیب‌یابی

### اگر همچنان HTTP 401 دریافت می‌کنید:

1. **بررسی Session:**
   ```python
   # در Django shell
   from django.contrib.sessions.models import Session
   Session.objects.all()
   ```

2. **بررسی Authentication:**
   ```python
   # در view
   print(request.user.is_authenticated)
   print(request.user)
   ```

3. **بررسی Headers:**
   - Developer Tools > Network
   - درخواست‌ها را بررسی کنید
   - Authorization header را چک کنید

## 💡 نکات مهم

- **Session Authentication** ساده‌ترین راه است
- **JWT Token** برای API calls مناسب است
- **Basic Authentication** برای تست سریع
- همیشه یکی از روش‌ها را انتخاب کنید

## 🎉 نتیجه

حالا می‌توانید:
- در REST framework لاگین کنید
- تمام API endpoints را مشاهده کنید
- درخواست‌های GET, POST, PUT, DELETE ارسال کنید
- از Browsable API استفاده کنید

### لینک‌های مفید:
- **API Login**: `http://127.0.0.1:8000/api/login/`
- **REST Framework**: `http://127.0.0.1:8000/api/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **JWT Login**: `http://127.0.0.1:8000/`


