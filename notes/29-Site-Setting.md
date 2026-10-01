# request.user.is_authenticated:

با این دستور در تمپلیت هایمان میتوانیم چک کنیم که اگر کاربر لاگین شده بود، به چه مواردی دسترسی داشته باشد و همچنین چک
کردیم اگر کاربر ایزسوپریوزر بود، یعنی ادمین کل بود، لینک پنل اصلی ادمین هم نمایش داده شود:

```
{% if request.user.is_authenticated %}
    {% if request.user.is_superuser %}
        <li><a href="/admin"><i class="fa fa-user"></i> پنل ادمین</a></li>
    {% endif %}
    <li><a href="#"><i class="fa fa-shopping-cart"></i> سبد خرید</a></li>
    <li><a href="#"><i class="fa fa-user"></i> پنل کاربری</a></li>
    <li><a href="{% url 'logout_page' %}"><i class="fa fa-sign-out"></i> خروج</a></li>
{% else %}
```

# Site Setting:

برای موارد مربوط به سایت، مثل اطلاعات و لینک های فوتر و ... معمولا میایم یک سایت ستینگ درنظر میگیریم؛ یعنی عملا یک جدول
داریم و این جدول، داخلش اطلاعات اصلی سایت، مثلا اطلاعات تماس، متن درباره ما، متن کپی رایت، تصویر لوگو و... در آن جدول
قرار میگیرند، در ابتدا باید یک سایت ماژول ایجاد کنیم:

1. `python manage.py startapp site_module`

2. کلاس مدل مربوط به تنظیمات سایت را پیاده سازی میکنیم:

```
class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name='نام سایت')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت')
    address = models.CharField(max_length=200, verbose_name='آدرس')
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name='تلفن')
    fax = models.CharField(max_length=200, null=True, blank=True, verbose_name='فکس')
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name='ایمیل')
    copy_right = models.TextField(verbose_name='متن کپی رایت سایت')
    about_us_text = models.TextField(verbose_name='متن درباره ما سایت')
    site_logo = models.ImageField(upload_to='images/site-setting/', verbose_name='لوگو سایت')
    is_main_setting = models.BooleanField(verbose_name='تنظیمات اصلی')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name
```

3. مایگریشن میزنیم تا جدول آن در دیتابیس ساخته شود

4. همیشه باید یک تنظیماتی ست کرده باشیم و مقدار فیلد تنظیمات اصلی آن ترو باشد، پس میریم داخل پنل ادمین و یک تنظیمات سایت
   جدید اضافه میکنیم که تنظیمات اصلی سایت ما باشد، در آینده هم میتونیم تنظیمات دیگری ایجاد کنیم برای شرایط مختلف و
   هرکدام را خواسته باشیم به عنوان تنظیمات اصلی ست کنیم.

5. در آخر هم میتونیم از این تنظیمات در سایت خودمان استفاده کنیم.
