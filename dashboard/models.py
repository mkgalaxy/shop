from django.db import models


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
    discount_price = models.BigIntegerField(null=True, blank=True, verbose_name="قیمت تخفیف‌خورده (شگفت‌انگیز)")
    stock = models.IntegerField(default=0, verbose_name="موجودی انبار")
    weight = models.IntegerField(default=0, verbose_name="وزن (گرم)")
    main_image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="تصویر اصلی")
    full_description = models.TextField(blank=True, null=True, verbose_name="توضیحات کامل محصول")

    is_flash_deal = models.BooleanField(default=False, verbose_name="نمایش در پیشنهادهای شگفت‌انگیز؟")
    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HomeSection(models.Model):
    """مدل مدیریت متن، تصویر و تنظیمات اختصاصی سکشن‌های صفحه اصلی"""
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

    # تنظیمات تایمر برای سکشن شگفت‌انگیزها
    timer_hours = models.IntegerField(default=7, verbose_name="ساعت تایمر")
    timer_minutes = models.IntegerField(default=38, verbose_name="دقیقه تایمر")
    timer_seconds = models.IntegerField(default=42, verbose_name="ثانیه تایمر")

    def __str__(self):
        return self.get_key_display()