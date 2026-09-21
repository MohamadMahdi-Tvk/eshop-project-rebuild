# Class Based View

زمانی که از کلاس بیس ویو خواسته باشیم استفاده کنیم، معمولا مرسوم هست که انتهای اسم کلاس کلمه ویو رو قرار بدهیم، که این
صرفا یک قرارداد است. پس ما یک کلاس بیس ویو بصورت زیر داریم:

```
class ContactUsView(View):
    def get(self, request):
        contact_form = ContactUsModelForm()
        return request(request, 'contact_module/contact_us_page.html', {
            'contact_form': contact_form
        })

    def post(self, request):
        contact_form = ContactUsModelForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect('home_page')

        return render(request, 'contact_module/contact_us_page.html', {
            'contact_form': contact_form
        })
```

سپس میریم آدرس آن هم ایجاد میکنیم؛ چون ویوی ما کلاس هست، و جنگو متوجه شود باید بعنوان یک ویو با این کلاس برخورد کند و
دستورات گت و پست آن را مدیریت کند، باید با دستور از ویو از آن استفاده کنیم، یعنی میگیم این کلاس رو بعنوان ویو درنظر
بگیر:

`path('', views.ContactUsView.as_view(), name='contact_us_page')`

پس در کلاس بیس ویو، اگر درخواست از نوع گت بهش ارسال شود، سیستم اتوماتیک متوجه میشود که باید بره متد گت داخل کلاس رو
فراخوانی کند و اگر درخواست از نوع پست باشد، میاد متد پست را فراخوانی میکند، مزیتی که دارد این هست که دیگه لازم نیست مثل
فانکشن بیس ویو بیایم و بصورت گزاره های شرطی این درخواست ها را جدا کنیم، اگر درخواست های دیگری مثل پوت و دیلیت هم بهش
اضافه شود، راحت میشود با آن کار کرد.

```
class HomeView(View):
    def get(self, request):
        return render(request, 'home_module/index_page.html')
```

## TemplateView

با این ساختار کلاس بیس ویو، دیگر لازم نیست برای دستور گت، فانکشن گت رو پیاده سازی کنیم؛ در زمان ارث بری از کلاس تمپلیت
ویو، یک گزینه تمپلیت نیم به کلاس اضافه میشود، بهش آدرس تمپلیت رو میدهیم:

```
class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'
```

پس در این نوع ساختار، بدون اینکه نیاز باشد تعریفی از دستور گت داشته باشیم و بگیم کدام تمپلیت رندر شود، به راحتی میتونیم
تمپلیت رو بهش پاس بدیم و خودش میره براساس دستور گت اون تمپلیت رو فراخوانی میکند و به کاربر نمایش میدهد.

### get_context_data ():

برای تنظیم کردن کانتکس در این نوع ساختار، میتونیم از اوراید کردن این متد استفاده کنیم، باید حتما داخل این فانکشن دستور
سوپر.گت کانتکس دیتا داخلش فراخوانی شود؛ ساختار کلی و پیش فرض متد به این شکل هست:

```
def get_context_data(self, **kwargs):
    return super().get_context_data(**kwargs)
```

برای اینکه داخل آن تغییرات خود را ایجاد کنیم یا یک آیتم جدید به کانتکس اضافه کنیم، مقدار سوپر به بعد را میریزیم داخل یک
متغییر با نام کانتکس و میگیم این کانتکس یک کلید جدیدی دارد مثلا تحت عنوان دیتا و مقدار برایش درنظر میگیریم:

```
class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = 'this is data in home page'
        context['message'] = 'this is message in home page'
        return context
```

حال در ویو میتونیم دیتا را نمایش دهیم:

`<p>{{ data }}</p>`
`<p>{{ message }}</p>`


## **kwargs

در تمپلیت ویو ها، اگر بخواهیم مقدار داینامیک پتس مثل اسلاگ برای صفحه ی جزئیات را بدست بیاوریم، یعنی همان سگمنت هایی که
بصورت داینامیک به آن آدرس ارسال میشوند، باید با استفاده از کیوردآرگومان هایی که به گت کانتکس دیتا ارسال میشوند این کار
را انجام دهیم:

```
class ProductDetailView(TemplateView):
    template_name = 'product_module/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        slug = kwargs['slug']
        product = get_object_or_404(Product, slug=slug)
        context['product'] = product
        return context
```