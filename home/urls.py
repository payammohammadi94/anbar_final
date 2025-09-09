from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('login/', views.login_page, name='login_page'),
]
