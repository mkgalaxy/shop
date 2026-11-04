from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Product, Category, HomeSection
from .forms import ProductForm, CategoryForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


def ensure_sections():
    """ایجاد ۶ سکشن اصلی صفحه در صورت عدم وجود"""
    defaults = [
        {'key': 'hero', 'title': 'تخفیف شگفت‌انگیز تکنولوژی', 'subtitle': 'بهترین تکنولوژی‌ها با بهترین قیمت',
         'button_text': 'مشاهده محصولات', 'button_link': '#'},
        {'key': 'categories', 'title': 'دسته‌بندی‌های سایت'},
        {'key': 'flash_deals', 'title': 'پیشنهادهای شگفت‌انگیز روزانه'},
        {'key': 'services', 'title': 'ارسال سریع و تضمین اصالت کالا'},
        {'key': 'products_grid', 'title': 'جدیدترین محصولات فروشگاه'},
        {'key': 'blog', 'title': 'مجله سبز و دانستنی‌ها'},
    ]
    for d in defaults:
        HomeSection.objects.get_or_create(key=d['key'], defaults=d)


@user_passes_test(is_admin)
def dashboard_home(request):
    ensure_sections()

    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('-id')
    sections = HomeSection.objects.all()

    edit_section = None
    if request.GET.get('edit_section'):
        edit_section = get_object_or_404(HomeSection, pk=request.GET.get('edit_section'))

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'save_product':
            pid = request.POST.get('product_id')
            inst = get_object_or_404(Product, pk=pid) if pid else None
            form = ProductForm(request.POST, request.FILES, instance=inst)
            if form.is_valid():
                form.save()
                return redirect('dashboard_home')

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

    context = {
        'products': products,
        'categories': categories,
        'sections': sections,
        'product_form': ProductForm(),
        'category_form': CategoryForm(),
        'edit_section': edit_section,
    }
    return render(request, 'dashboard/index.html', context)