# CreateView

در این ساختار، دیگر لازم نیست بیایم و فرم کلاس را مشخص کنیم، فقط کافیست مشخص کنیم از کدام مدل میخواهیم استفاده کنیم؛ اگر
هم فیلد خاصی مد نظر داریم، مشخص میکنیم؛ پس هم میشود خود مدل را بدهیم و یا فرمی که ایجاد کرده ایم را به فرم کلاس بدهیم؛
فرم کلاس هم باید حتما از نوع مدل فرم باشد، اگر مدل فرم پاس بدهیم، قابلیت هایی که در فرمز پیاده سازی کرده ایم مثل کلاس ها
و لیبل ها را خواهیم داشت؛ پس بصورت کلی به این شکل میتونیم ویوی کریت خود را بسازیم:

```
class ContactUsView(CreateView):
    model = ContactUs
    form_class = ContactUsModelForm
    template_name = 'contact_module/contact_us_page.html'
    success_url = '/contact_us/'
```

الزامی ندارد که مدل را معرفی کنیم، چون که در کانتکس آس مدل فرم، مدل خود را معرفی کرده ایم:

```
class ContactUsView(CreateView):
    form_class = ContactUsModelForm
    template_name = 'contact_module/contact_us_page.html'
    success_url = '/contact_us/'
```

# UpdateView, DeleteView

ما این ویو ها را هم داریم، ولی ساختار آنها شبیه به همدیگر هست و در داکیومنت رسمی میتوان جزئیات بیشتری از آنها یاد گرفت.

# File Upload

1. اگر ما یک فرمی داریم که داخل آن یک اینپوت از نوع فایل هست و قرار هست به سمت سرور ارسال شود، حتما باید برای آن فرم در
   تگ فرم انکریپت تایپ درنظر بگیریم، با مقدار زیر:

`enctype="multipart/form-data"`

2. و باید در فایل تمپلیت ما، یک اینپوت از جنس فایل وجود داشته باشد و یک اسم هم بهش میدهیم:

`<input type="file" name="profile">`

3. در فانکشن پست، یعنی وقتی عکس انتخاب شده و روی ارسال کلیک میکنیم، یک دستور رکوئست.فایلز داریم که اطلاعات آن فایل را
   دریافت میکند:

```
class CreateProfileView(View):
    def get(self, request):
        return render(request, 'contact_module/create_profile_page.html')

    def post(self, request):
        print(request.FILES)
        return redirect('/contact-us/create-profile')
```

4. در خروجی ترمینال خروجی زیر را میبینیم با همان اسمی که در اینپوت نام فایل داده بودیم، یعنی نام پروفایل:

`<MultiValueDict: {'profile': [<InMemoryUploadedFile: 5825786.jpg (image/jpeg)>]}>`


