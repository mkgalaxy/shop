from django.db import models
from django.conf import settings  # جایگزین ایمپورت مستقیم User


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="نام دسته")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name="دسته والد")
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name="تصویر دسته")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام محصول")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="دسته‌بندی")
    price = models.BigIntegerField(verbose_name="قیمت (تومان)")
    discount_price = models.BigIntegerField(null=True, blank=True, verbose_name="قیمت تخفیف‌خورده")
    stock = models.IntegerField(default=0, verbose_name="موجودی انبار")
    weight = models.IntegerField(default=0, verbose_name="وزن (گرم)")
    main_image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="تصویر اصلی")
    full_description = models.TextField(blank=True, null=True, verbose_name="توضیحات کامل محصول")

    # فیلدهای سئو (Rank Math) برای محصولات
    meta_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="عنوان سئو")
    meta_description = models.TextField(blank=True, null=True, verbose_name="توضیحات متاسئو")
    focus_keyword = models.CharField(max_length=100, blank=True, null=True, verbose_name="کلمه کلیدی اصلی")

    is_flash_deal = models.BooleanField(default=False, verbose_name="پیشنهاد شگفت‌انگیز؟")
    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HomeSection(models.Model):
    KEY_CHOICES = (
        ('hero', 'بنر اصلی (هیرو)'),
        ('categories', 'سکشن دسته‌بندی‌ها'),
        ('flash_deals', 'پیشنهادهای شگفت‌انگیز'),
        ('services', 'سکشن خدمات و ارسال'),
        ('products_grid', 'جدیدترین محصولات'),
        ('blog', 'مجله و دانستنی‌ها'),
    )
    key = models.CharField(max_length=50, unique=True, choices=KEY_CHOICES, verbose_name="کلید سکشن")
    title = models.CharField(max_length=255, verbose_name="عنوان سکشن")
    subtitle = models.TextField(blank=True, null=True, verbose_name="توضیحات / زیرعنوان")
    image = models.ImageField(upload_to='sections/', blank=True, null=True, verbose_name="تصویر سکشن")
    button_text = models.CharField(max_length=100, blank=True, null=True, verbose_name="متن دکمه")
    button_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="لینک دکمه")

    timer_hours = models.IntegerField(default=7, verbose_name="ساعت تایمر")
    timer_minutes = models.IntegerField(default=38, verbose_name="دقیقه تایمر")
    timer_seconds = models.IntegerField(default=42, verbose_name="ثانیه تایمر")

    def __str__(self):
        return self.title


class BlogCategory(models.Model):
    name = models.CharField(max_length=150, verbose_name="عنوان دسته‌بندی بلاگ")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="نام در URL")

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان مقاله")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="نام در URL (اسلاگ)")
    # اصلاح ارتباط نویسنده با مدل کاربر پروژه
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="نویسنده")
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts',
                                 verbose_name="دسته‌بندی بلاگ")
    image = models.ImageField(upload_to='blog/', null=True, blank=True, verbose_name="تصویر شاخص")
    content = models.TextField(verbose_name="محتوای مقاله")

    # فیلدهای سئو (Rank Math)
    focus_keyword = models.CharField(max_length=100, blank=True, null=True, verbose_name="کلمه کلیدی اصلی")
    meta_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="عنوان سئو")
    meta_description = models.TextField(blank=True, null=True, verbose_name="توضیحات متاسئو")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title