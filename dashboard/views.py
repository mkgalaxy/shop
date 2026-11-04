from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Product, Category, HomeSection, BlogPost, BlogCategory
from .forms import ProductForm, CategoryForm, BlogPostForm, BlogCategoryForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


def ensure_sections():
    defaults = [
        {'key': 'hero', 'title': 'تخفیف شگفت‌انگیز تکنولوژی', 'subtitle': 'بهترین تکنولوژی‌ها با بهترین قیمت',
         'button_text': 'مشاهده محصولات', 'button_link': '#'},
        {'key': 'categories', 'title': 'دسته‌بندی‌های سایت'},
        {'key': 'flash_deals', 'title': 'پیشنهادهای شگفت‌انگیز روزانه'},
        {'key': 'services', 'title': 'ارسال سریع و تضمین اصالت کالا'},
        {'key': 'products_grid', 'title': 'جدیدترین محصولات فروشگاه'},
        {'key': 'blog', 'title': 'مجله و دانستنی‌ها'},
    ]
    for d in defaults:
        HomeSection.objects.get_or_create(key=d['key'], defaults=d)


@user_passes_test(is_admin)
def dashboard_home(request):
    ensure_sections()

    # استخراج تمام اطلاعات دیتابیس
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('-id')
    sections = HomeSection.objects.all()
    blog_posts = BlogPost.objects.select_related('category', 'author').order_by('-created_at')
    blog_categories = BlogCategory.objects.all()

    # حالات ویرایش (Editing instances)
    edit_product = None
    edit_category = None
    edit_section = None
    edit_post = None

    if request.GET.get('edit_product'):
        edit_product = get_object_or_404(Product, pk=request.GET.get('edit_product'))
        product_form = ProductForm(instance=edit_product)
    else:
        product_form = ProductForm()

    if request.GET.get('edit_category'):
        edit_category = get_object_or_404(Category, pk=request.GET.get('edit_category'))
        category_form = CategoryForm(instance=edit_category)
    else:
        category_form = CategoryForm()

    if request.GET.get('edit_section'):
        edit_section = get_object_or_404(HomeSection, pk=request.GET.get('edit_section'))

    if request.GET.get('edit_post'):
        edit_post = get_object_or_404(BlogPost, pk=request.GET.get('edit_post'))
        blog_form = BlogPostForm(instance=edit_post)
    else:
        blog_form = BlogPostForm()

    blog_category_form = BlogCategoryForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        # ۱. مدیریت محصولات
        if action == 'save_product':
            pid = request.POST.get('product_id')
            inst = get_object_or_404(Product, pk=pid) if pid else None
            form = ProductForm(request.POST, request.FILES, instance=inst)
            if form.is_valid():
                form.save()
                return redirect('dashboard_home')

        elif action == 'delete_product':
            Product.objects.filter(pk=request.POST.get('product_id')).delete()
            return redirect('dashboard_home')

        # ۲. مدیریت دسته‌بندی محصولات
        elif action == 'save_category':
            cid = request.POST.get('category_id')
            inst = get_object_or_404(Category, pk=cid) if cid else None
            form = CategoryForm(request.POST, request.FILES, instance=inst)
            if form.is_valid():
                form.save()
                return redirect('dashboard_home')

        elif action == 'delete_category':
            Category.objects.filter(pk=request.POST.get('category_id')).delete()
            return redirect('dashboard_home')

        # ۳. مدیریت سکشن‌های صفحه اصلی
        elif action == 'save_section':
            sec_id = request.POST.get('section_id')
            sec = get_object_or_404(HomeSection, pk=sec_id)
            sec.title = request.POST.get('title', '')
            sec.subtitle = request.POST.get('subtitle', '')
            sec.button_text = request.POST.get('button_text', '')
            sec.button_link = request.POST.get('button_link', '')

            if 'image' in request.FILES:
                sec.image = request.FILES['image']

            if request.POST.get('timer_hours'):
                sec.timer_hours = int(request.POST.get('timer_hours'))
            if request.POST.get('timer_minutes'):
                sec.timer_minutes = int(request.POST.get('timer_minutes'))
            if request.POST.get('timer_seconds'):
                sec.timer_seconds = int(request.POST.get('timer_seconds'))

            sec.save()
            return redirect('dashboard_home')

        # ۴. مدیریت مقالات بلاگ
        elif action == 'save_post':
            post_id = request.POST.get('post_id')
            post_inst = get_object_or_404(BlogPost, pk=post_id) if post_id else None
            b_form = BlogPostForm(request.POST, request.FILES, instance=post_inst)
            if b_form.is_valid():
                post = b_form.save(commit=False)
                if not post_inst:
                    post.author = request.user
                post.save()
                return redirect('dashboard_home')

        elif action == 'delete_post':
            BlogPost.objects.filter(pk=request.POST.get('post_id')).delete()
            return redirect('dashboard_home')

        # ۵. مدیریت دسته‌بندی‌های بلاگ
        elif action == 'save_blog_category':
            bc_form = BlogCategoryForm(request.POST)
            if bc_form.is_valid():
                bc_form.save()
                return redirect('dashboard_home')

    context = {
        'products': products,
        'categories': categories,
        'sections': sections,
        'blog_posts': blog_posts,
        'blog_categories': blog_categories,
        'product_form': product_form,
        'category_form': category_form,
        'blog_form': blog_form,
        'blog_category_form': blog_category_form,
        'edit_product': edit_product,
        'edit_category': edit_category,
        'edit_section': edit_section,
        'edit_post': edit_post,
    }
    return render(request, 'dashboard/index.html', context)