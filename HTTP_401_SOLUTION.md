# راهنمای حل مشکل HTTP 401 Unauthorized

## 🔍 تشخیص مشکل

اگر با وجود لاگین موفق، همچنان خطای HTTP 401 دریافت می‌کنید، مشکل در ارسال توکن JWT در درخواست‌های API است.

## ✅ راه‌حل‌های مختلف

### 1. استفاده از صفحه لاگین بهبود یافته

صفحه لاگین حالا قابلیت تست API را دارد:

1. به `http://127.0.0.1:8000/` بروید
2. وارد شوید
3. بخش "تست API" نمایش داده می‌شود
4. روی دکمه‌های تست کلیک کنید تا API را تست کنید

### 2. استفاده از Postman یا Insomnia

#### تنظیمات Header:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

#### مثال درخواست:
```
GET http://127.0.0.1:8000/api/categories/
Headers:
  Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
  Content-Type: application/json
```

### 3. استفاده از cURL

```bash
# دریافت توکن
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'

# استفاده از توکن
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://127.0.0.1:8000/api/categories/
```

### 4. استفاده از JavaScript (Frontend)

```javascript
// دریافت توکن
const loginResponse = await fetch('/api/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'admin',
        password: 'your_password'
    })
});

const tokens = await loginResponse.json();
const accessToken = tokens.access;

// استفاده از توکن در درخواست‌های API
const apiResponse = await fetch('/api/categories/', {
    headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
    }
});

const data = await apiResponse.json();
console.log(data);
```

### 5. استفاده از Python

```python
import requests

# دریافت توکن
login_data = {
    "username": "admin",
    "password": "your_password"
}

login_response = requests.post('http://127.0.0.1:8000/api/auth/login/', json=login_data)
tokens = login_response.json()
access_token = tokens['access']

# استفاده از توکن
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

api_response = requests.get('http://127.0.0.1:8000/api/categories/', headers=headers)
data = api_response.json()
print(data)
```

## 🔧 عیب‌یابی

### بررسی توکن:
1. توکن را در `https://jwt.io` بررسی کنید
2. مطمئن شوید توکن منقضی نشده باشد
3. بررسی کنید که توکن کامل کپی شده باشد

### بررسی Header:
```javascript
// بررسی Header در Developer Tools
console.log('Authorization Header:', 'Bearer ' + localStorage.getItem('access_token'));
```

### تست ساده:
```bash
# تست مستقیم با cURL
curl -v -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/categories/
```

## 📋 چک‌لیست حل مشکل

- [ ] کاربر ادمین ایجاد شده است
- [ ] سرور Django اجرا شده است
- [ ] توکن JWT دریافت شده است
- [ ] توکن در Header ارسال می‌شود
- [ ] فرمت Header صحیح است: `Bearer TOKEN`
- [ ] توکن منقضی نشده است
- [ ] درخواست به endpoint صحیح ارسال می‌شود

## 🚀 تست سریع

1. به `http://127.0.0.1:8000/` بروید
2. وارد شوید
3. روی "تست دسته‌بندی‌ها" کلیک کنید
4. اگر موفق بود، مشکل حل شده است!

## 📞 در صورت ادامه مشکل

اگر همچنان مشکل دارید:

1. Console مرورگر را بررسی کنید
2. Network tab را در Developer Tools چک کنید
3. مطمئن شوید سرور Django اجرا شده است
4. بررسی کنید که JWT settings درست پیکربندی شده است

## 💡 نکات مهم

- توکن JWT پس از 1 روز منقضی می‌شود
- برای تمدید توکن از `/api/auth/refresh/` استفاده کنید
- همیشه توکن را در Header ارسال کنید
- فرمت صحیح: `Authorization: Bearer TOKEN`


