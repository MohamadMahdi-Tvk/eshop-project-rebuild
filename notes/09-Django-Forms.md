# Django Forms

## Validation:

### ساده ترین روش پیاده سازی یک اعتبارسنجی:

اعتبارسنجی یکی از مباحث مهم در پروژه هست، به این دلیل که کاربر نباید این اجازه رو داشته باشد که هر مقداری را به سرور
ارسال کند، و ما میتوانیم در همان فایل ویو آن را چک کنیم و در ویو یک اخطاری به کاربر بدهیم مثلا میتوانیم بگوییم اگر ایمیل
خالی بود، یک پیغامی به کاربر در ویو نمایش داده شود؛ در پروژه های واقعی عملا این روش به درد نمیخورد، اما در یکسری شرایط
خاص میتوان از این روش استفاده کرد:

```
def contact_us_page(request):
    if request.method == 'POST':
        entered_email = request.POST['email']
        if entered_email == '':
            return render(request, 'contact_module/contact_us_page.html', {
                'has_error' : True
            })
        print(request.POST['email'])
        print(request.POST['fullname'])
        print(request.POST['subject'])
        print(request.POST['message'])
        return redirect(reverse('home_page'))
    return render(request, 'contact_module/contact_us_page.html', {
        'has_error' : False
    })
```

و از آنطرف در فایل ویو:

```
{% if has_error %}
  <p class="alert alert-warning">لطفا ایمیل خود را وارد نمایید</p>
{% endif %}
```

### روش عالی تر برای پیاده سازی اعتبارسنجی ها:

ابتدا یک فایل پایتون با نام فرمز در اپ خود ایجاد میکنیم؛ داخلش یک کلاس ایجاد کرده و ساختار این کلاس فرم یک چیزی تقریبا
شبیه به مدل های ما هست، یعنی باید اینپوت ها و نوعش را مشخص کنیم و ولیدیشن هم برایش درنظر بگیریم پس داخل بدنه کلاس،
فیلدهایی که نیاز داریم رو طراحی کنیم:

```
from django import forms


class ContactUsForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    text = forms.CharField()
```

سپس باید بریم داخل فایل پایتون ویو و کد هایمان را ویرایش کنیم، اول باید یک نمونه از کلاس فرم ایجاد کنیم و آنرا به کانتکس
پاس دهیم

```
def contact_us_page(request):
    if request.method == 'POST':
        contact_form = ContactUsForm(request.POST)
        if contact_form.is_valid():
            print(contact_form.cleaned_data)
            return redirect('home_page')

    contact_form = ContactUsForm()
    return render(request, 'contact_module/contact_us_page.html', {
        'contact_form': contact_form
    })

```

از آن طرف در ویو، دیگر لازم نیست اینپوتی داشته باشیم، فقط اینپوت ها را بر داشته و بجایش فقط و فقط این دستور را در صفحه
قرار میدهیم با این کار، بصورت اتوماتیک فیلد های ما درون فرم قرار میگیرند و دیگر نیازی نیست خودمان در صفحه تگ های اینپوت
قرار بدهیم و خود جنگو این کار را انجام میدهد و این یکی از قدرت ها جنگو است حتی اتربیوت های آن هم جنگو تولید میکند:
`{{ contact_form }}`

نکات دیگر:
`contact_form = ContactUsForm(request.POST)`:
در این دستور اتوماتیک میره دیتا را برمیدارد و در کانتکت فرم در قالب یک شی بهش دسترسی داریم

is_valid: این دستور میاد چک میکند که آیا آیتم های موجود درون آن فرم، همه شون معتبر هستند و میتونیم با همین دستور چک کنیم
اگر همه چی اوکی بود، بیاد عملیات ذخیره سازی در دیتابیس را انجام دهد
`if contact_form.is_valid():`

cleaned_data: تمامی اطلاعاتی که درون فرم هست رو برمیگرداند
`print(contact_form.cleaned_data)`
این دستور، میاد در قالب یک دیکشنری اطلاعات فیلد های جدول را در ترمینال نمایش میدهد، به این شکل:
{'full_name': 'محمدمهدی توکلی', 'email': 'mohamadmahditavakoli8@gmail.com', 'subject': 'برنامه نویسی', 'text': 'متن تستی'}

قابلیت هایی که این فرم برایمان فراهم میکند، خیلی بیشتر از این حرفاست، میتونیم این فرم را مستقیم به یک مدل متصل کنیم
یا میتوانیم ارور های احتمالی را به کاربر نمایش بدهیم، یا برای اینپوت ها لیبل قرار بدهیم و غیره.