from django.shortcuts import render, get_object_or_404
from dashboard.models import Category, Product, HomeSection, BlogPost, BlogCategory


def home(request):
    categories = Category.objects.all()
    sec = {s.key: s for s in HomeSection.objects.all()}

    # دریافت جدیدترین محصولات فروشگاه
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:3]

    # دریافت محصولات شگفت‌انگیز
    flash_deals = Product.objects.filter(is_active=True, is_flash_deal=True)[:4]
    if not flash_deals.exists():
        flash_deals = Product.objects.filter(is_active=True, discount_price__isnull=False)[:4]

    # دریافت آخرین مقالات بلاگ برای نمایش در سکشن مجله صفحه اصلی
    latest_posts = BlogPost.objects.select_related('author', 'category').order_by('-created_at')[:3]

    context = {
        'categories': categories,
        'latest_products': latest_products,
        'flash_deals': flash_deals,
        'latest_posts': latest_posts,
        'sec': sec,
    }
    return render(request, 'shop/index.html', context)


def category_products(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(is_active=True, category=category).order_by('-created_at')
    return render(request, 'shop/category_products.html', {'category': category, 'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    return render(request, 'shop/product_detail.html', {'product': product})


def blog_list(request):
    posts = BlogPost.objects.select_related('author', 'category').order_by('-created_at')
    blog_categories = BlogCategory.objects.all()
    return render(request, 'shop/blog_list.html', {'posts': posts, 'blog_categories': blog_categories})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    related_posts = BlogPost.objects.filter(category=post.category).exclude(id=post.id)[:3]
    return render(request, 'shop/blog_detail.html', {'post': post, 'related_posts': related_posts})