# Choices

یکی از پارمتر هایی که ما میتوانیم به کرفیلد یا اینتیجرفیلد ها در کلاس های مدل خود پاس بدیم، چویسز هست؛ این چویسز، یک
لیست میگیرد؛ یعنی خیلی راحت ما میتوانیم یک لیست از توپل ها تعریف کنیم؛ در هر توپل دو تا آیتم در نظر گرفته میشود، آیتم
اول کلید و آیتم دوم، مقدار نمایشی آن است؛ یعنی آن چیزی که در دیتابیس ذخیره میشود، آیتم اول توپل است و آن چیزی که در دراپ
داون به کاربر نمایش داده میشود، آیتم دوم توپل است:

```
site_banner_positions = [
    ('product_list', 'صفحه لیست محصولات'),
    ('product_detail', 'صفحه جزییات محصولات')
]

class SiteBanner(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان بنر')
    url = models.URLField(max_length=400, null=True, blank=True, verbose_name='آدرس بنر')
    image = models.ImageField(upload_to='images/banners', verbose_name='تصویر بنر')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    position = models.CharField(max_length=200, choices=site_banner_positions, verbose_name='جایگاه نمایشی')
```

## Choices - Second Way

اما الان یک مشکل کوچکی داریم، فرض کنیم چندین برنامه نویس روی پروژه کار میکنند و دراپ داونی هم که درنظر گرفته شده آیتم
های زیادی داشته باشد، حفظ کردن این آیتم ها دردسر خواهد داشت، روش جایگزینی هم هست؛ به این صورت که در کلاس مدل خود
میتوانیم یک ساب کلاس ایجاد کرده و آیتم ها را بصورت کلاس فیلد برایش تعریف کنیم و اون ساب کلاس باید از مدلز.تکست چویسز ارث
بری کرده باشد؛ پس به این روش هم میتوانیم خیلی راحت فیلد های دراپ داون خود را مشخص کنیم:

```
class SiteBanner(models.Model):
    class SiteBannerPositions(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات',
        product_detail = 'product_detail', 'صفحه جزییات محصولات',
        about_us = 'about_us', 'درباره ما'

    title = models.CharField(max_length=200, verbose_name='عنوان بنر')
    url = models.URLField(max_length=400, null=True, blank=True, verbose_name='آدرس بنر')
    image = models.ImageField(upload_to='images/banners', verbose_name='تصویر بنر')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    position = models.CharField(max_length=200, choices=SiteBannerPositions.choices, verbose_name='جایگاه نمایشی')
```

میتوان در ویو به مقادیر چویسز دسترسی داشته باشیم و آن را با کانتکس به صفحه ارسال کنیم:

`context['banners'] = SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.SiteBannerPositions.product_list)`

و آن طرف در صفحه میتوان از آن کانتکسی که از ویو فرستادیم، استفاده کنیم:

```
{% for banner in banners %}
    <a href="{{ banner.url }}">
        <img src="{{ banner.image.url }}" alt="">
    </a>
{% endfor %}
```

