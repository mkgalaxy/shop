from django.shortcuts import render, get_object_or_404
from dashboard.models import Category, Product, HomeSection


def home(request):
    categories = Category.objects.all()

    # استخراج تمام ۶ سکشن به صورت دیکشنری بر اساس کلید سکشن
    sections_qs = HomeSection.objects.all()
    sec = {s.key: s for s in sections_qs}

    # ۱. جدیدترین محصولات: ۳ محصول آخر اضافه شده به سایت به صورت خودکار
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:3]

    # ۲. پیشنهادهای شگفت‌انگیز: محصولاتی که دارای قیمت تخفیف‌خورده هستند یا تیک شگفت‌انگیز دارند
    flash_deals = Product.objects.filter(is_active=True, discount_price__isnull=False, is_flash_deal=True)[:4]
    if not flash_deals.exists():
        flash_deals = Product.objects.filter(is_active=True, discount_price__isnull=False)[:4]

    context = {
        'categories': categories,
        'latest_products': latest_products,
        'flash_deals': flash_deals,
        'sec': sec,
    }
    return render(request, 'shop/index.html', context)


def category_products(request, category_id):
    """صفحه اختصاصی محصولات یک دسته‌بندی خاص (مثلاً موبایل)"""
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(is_active=True, category=category).order_by('-created_at')

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'shop/category_products.html', context)


def product_detail(request, product_id):
    """صفحه توضیحات کامل محصول"""
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    return render(request, 'shop/product_detail.html', {'product': product})