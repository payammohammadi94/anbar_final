from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

# Create your views here.

def login_page(request):
    """صفحه لاگین"""
    return render(request, 'home/login.html')

@method_decorator(csrf_exempt, name='dispatch')
class APILoginView(View):
    """View برای لاگین API"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return JsonResponse({'error': 'نام کاربری و رمز عبور الزامی است'}, status=400)
            
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({'message': 'ورود موفقیت‌آمیز'})
            else:
                return JsonResponse({'error': 'نام کاربری یا رمز عبور اشتباه است'}, status=401)
                
        except Exception as e:
            return JsonResponse({'error': 'خطا در پردازش درخواست'}, status=500)
