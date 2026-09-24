# Upload Image

## ImageField

برای آپلود فقط تصویر میتونیم از این مورد در تعریف کلاس های مدل استفاده کنیم؛ اما برای استفاده از ایمیج فیلد باید پکیج
پیلو استفاده کنیم:

```
class UserProfile(models.Model):
    image = models.ImageField(upload_to='images')
```

## Pillow Package:

1. `pip install pillow`

2. در اجرا، وقتی میخوایم فایل آپلود کنیم، فقط و فقط تصویر قبول میکند، ویو را هم به این شکل باید تغییر دهیم:

```
class CreateProfileView(CreateView):
    template_name = 'contact_module/create_profile_page.html'
    model = UserProfile
    fields = '__all__'
    success_url = '/contact-us/create-profile/'
```

## نمایش تصاویر

1. یک ویو برای نمایش تصاویر میسازیم:

```
class ProfilesView(ListView):
    model = UserProfile
    template_name = 'contact_module/profiles_list_page.html'
    context_object_name = 'profiles'
```

2. داخل تگ های اچتی ام ال میتونیم از ایمیج استفاده کنیم، وقتی که دات رو بعد از ایمیج بزنیم، هم میتونیم از یوآرال استفاده
   کنیم و هم از پتس، پتس اشاره میکند به آدرس سیستمی آن تصویر که در سرور ذخیره شده است، اما اگر بخوایم آدرس پاس بدیم با
   یوآرال این کار را میکنیم، یعنی خودش یوآرال را جنریت میکند:

```
{% extends 'shared/_layout.html' %}

{% block title %}
    لیست پروفایل ها
{% endblock %}

{% block content %}
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <ul>
                    {% for profile in profiles %}
                    	<li>
                            <img src="{{ profile.image.url }}" alt="" width="200">
                        </li>
                    {% endfor %}
                    
                </ul>
            </div>
        </div>
    </div>
{% endblock %}
```

3. اما اگر همین صفحه را باز کنیم، عکس ها لود نشده اند، به این دلیل که جنگو، بنابر تنظیمات امنیتی که براش درنظر گرفته شده
   است، آدرس پوشه های درون خودش رو لاک میکند، برای اینکه کسی نتواند از طریق یوآرال به فایل های پروژه دسترسی داشته باشد،
   درسته که در فایل ستینگ، مدیتا روت را تعریف کرده ایم که آن بخاطر تنظیمات داخلی جنگو بود، اما موقع سرو کردن باید
   تنظیمات دیگری را انجام دهیم، این تنظیمات با نام مدیا یوآر ال هست، که یک آدرسی بهش میدیم مثل مدیاز و هر آدرسی که
   بخواهیم جنریت کنیم، مثل آدرسی که برای تصاویر جنریت شده اند، قبلش کلمه مدیاز انداخته میشود و جنگو متوجه میشود این آدرس
   ها باید خوانده شوند؛ پس این دو تنظیم لازم هستند:

```
MEDIA_ROOT = BASE_DIR / 'uploads'
MEDIA_URL = '/medias/'
```

4. در این مرحله باید به سیستم مسریابی هم معرفی کنیم، پس باید به یوآرال اصلی پروژه برویم و آنرا کانفیگ کنیم، پس به یوآرال
   پترنز باید فانکشن استاتیک رو اضافه کنیم، ورودی اول همان مدیا یوآرال هست، ورودی دوم داکیومنت روت را دریافت میکند که
   مشخص میکنیم آدرسی که بهش داده میشه رو باید از داخل کدام پوشه بگردد دنبال آیتم ها، که مدیا روت رو پاس میدیم:

```
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('', include('home_module.urls')),
    path('contact-us/', include('contact_module.urls')),
    path('products/', include('product_module.urls')),
    path('admin/', admin.site.urls)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)T)

```

در نتیجه یوآرالی که در تگ ایمیج قرار داده شده، اشاره میکند به همان آدرسی که در دیتابیس ذخیره شده است، یعنی آدرس فایل رو
برمیگرداند، و بخاطر موارد امنیتی، جنگو میاد دسترسی به آن فایل ها را از طریق یوآر ال محدود میکند، به همین دلیل رفتیم داخل
فایل ستینگ و مدیا یوآرال تنظیم کردیم و جفت مدیا روت و مدیا یوآرال رو باید داخل یوآرال های اصلی اپلیکیشن تعریف کنیم که
بتونیم ازش خروجی بگیریم و فایل های مدیای ما در پروژه قابل استفاده باشند.