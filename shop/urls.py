from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # مسیرهای بخش وبلاگ (تغییر slug به str جهت پشتیبانی از کاراکترهای فارسی)
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<str:slug>/', views.blog_detail, name='blog_detail'),
]