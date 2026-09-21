# Detail View

برای نمایش جزئیات یک آیتم، مثل نمایش جزئیات یک محصول، یک کلاس بیس ویو دیگری داخل جنگو وجود دارد به اسم دیتیل ویو که باز
هم کلاسی ایجاد کرده و از آن ارث بری میکنیم و باز هم نام تمپلیت و مدل خود را بهش معرفی میکنیم، برای پروداکت اومدیم از
اسلاگ فیلد داخل یوآرال استفاده کردیم، دیتیل ویو بوسیله همین اسلاگ فیلد، خودش متوجه میشود و آیتم را پیدا میکند؛ پس ما یا
باید از اسلاگ فیلد استفاده کنیم یا از آیدی:

```
from django.views.generic import ListView, DetailView

class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product
   
```

معرفی یو آر ال به شکل زیر باید باشد:

`path('<slug:slug>', views.ProductDetailView.as_view(), name='product_detail')`

اگر پیدا کردن محصول براساس آیدی بود باید حتما از کلمه کلیدی پی کی استفاده کنیم و یوآرال باید به این شکل باشد:

`path('<int:pk>', views.ProductDetailView.as_view(), name='product_detail')`



# Form View

یک کلاس بیس ویوی دیگر برای کار کردن با فرم ها هست که کار ما را به شدت راحت تر میکند و کدنویسی کمتری هم داریم و کافیست
اسم تمپلیت را بهش پاس دهیم و فرم کلاس، یعنی همان فرمی که در فایل فرمز ایجاد کرده بودیم؛ و در آخر هم باید حتما برایش یک
ساکسز یوآرال مشخص کنیم، برای اینکه زمانی که فرم به درستی سابمیت شد و همه چی اوکی بود، کاربر به کجا ریدایرکت شود؛ سپس
باید با دو فانکشن مشخص کنیم اگر فرم ولید و معتبر بود چه اتفاقی بیفتد که فرم را سیو میکنیم و اگر اینولید بود چه اتفاقی که
بعد از پیاده سازی این موارد، در نهایت فرم ما به درستی ایجاد میشود و دیتا را ذخیره میکند:

```
from django.views.generic.edit import FormView

class ContactUsView(FormView):
    template_name = 'contact_module/contact_us_page.html'
    form_class = ContactUsModelForm
    success_url = '/contact-us/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
```

کد های تمپلیت هم به این صورت میشوند:

```
<div class="col-md-6 form-group">
    {{ form.email.label_tag }}
    {{ form.email }}
    {{ form.email.errors }}
</div>

<div class="col-md-6 form-group">
    {{ form.full_name.label_tag }}
    {{ form.full_name }}
    {{ form.full_name.errors }}
</div>

<div class="col-md-12 form-group">
    {{ form.title.label_tag }}
    {{ form.title }}
    {{ form.title.errors }}
</div>


<div class="col-md-12 form-group">
    {{ form.message.label_tag }}
    {{ form.message }}
    {{ form.message.errors }}
</div>
```