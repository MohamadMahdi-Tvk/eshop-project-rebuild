# Django Forms Customization

## widgets:

یک دیکشنری هست که عملا برای کلید هایی که برای قسمت فیلدز در کلاس خود درنظر گرفته ایم، میتوانیم کانفیگ دلخواهی را اعمال
کنیم و میتوانیم اتربیوت هاش رو مشخص کنیم که باز هم یک دیکشنری هست و میتوان مواردی مثل کلاس بهش اختصاص داد:

```
class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'title', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'id': 'message',
            })
        }
```

## labels:

میتوان در همین کلاس لیبل های فرم برای هر فیلد هم شخصی سازی کنیم:

```
labels = {
    'full_name': 'نام و نام خانوادگی شما',
    'email' : 'ایمیل شما'
}
```

## error_messages:

در همین کلاس پیام های ارور برای هر فیلد هم میتوانیم شخصی سازی کنیم؛ یعنی برای هر فیلد و هر اعتبارسنجی مربوط به آن:

```
error_messages = {
    'full_name': {
    'required': 'نام و نام خانوادگی اجباری می باشد، لطفا آن را وارد کنید'
}
```

## contact_form.save ()

کافیست فقط این دستور را در ویو فراخوانی کنیم تا دیتا ذخیره شود، به این دلیل هست که ما اومدیم از مدل فرم استفاده کردیم:

```
def contact_us_page(request):
    if request.method == 'POST':
        contact_form = ContactUsModelForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()

            return redirect('home_page')
    else:
        contact_form = ContactUsModelForm()

    return render(request, 'contact_module/contact_us_page.html', {
        'contact_form': contact_form
    })
```

## instance:

نمونه ای که از فرم در ویو ساخته میشود، میتواند یک پارامتر ورودی دیگر تحت عنوان اینستنس بگیرد؛ یعنی مدل فرم ما عملا
میتواند عملیات ویرایش را هم برامون انجام دهد. که بعدا در جای مناسب پیاده سازی آن را انجام خواهیم داد.

# class base view:

ما تا الان هر ویویی که ساختیم، همه شون فانکشن بیس بودند و داخلش باید چک میکردیم دستور از نوع پست هست یا گت و یک مقداری
دردسر داشت، به همین دلیل در فریمورک جنگو، یک قابلیتی رو ایجاد کردند، تحت عنوان کلاس بیس ویو؛ و این ساختار امکانات خیلی
جذابی رو برای ما فراهم کرده است. یعنی کافیست ما کلاس را ایجاد کرده از ویو ارث بری کرده و سپس فانکشن های مدنظر خودمون مثل
گت، پست را داخل این کلاس پیاده سازی کنیم، که این متد ها همان متد های اچ تی تی پی ما هستند و زمانی که درخواست به سمت این
کلاس ارسال میشود، اتوماتیک خودش متوجه میشود که گت را باید ارسال کند یا پست را فراخوانی کند؛ مثلا در کد زیر میگیم اگر گت
فراخوانی شد بیا فرم رو بساز و ویوی داده شده رو برگردان و در دستور پست هم اطلاعات رو در دیتابیس ذخیره میکنیم:

```
from django.views import View

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