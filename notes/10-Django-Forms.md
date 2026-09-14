# Django Forms - Part 2

## پر ماندن دیتای فیلد ها پس از ارسال درخواست و دریافت خطای فیلد ها:

در فانکشن خود میتوان کاری کنیم که در الس اگر حالت گت بود، فیلد های پر شده باقی بمانند و از بین نروند و اینکه متن خطای
مربوط به فیلد مثلا مقدار این فیلد لازم هست را هم میاورد پس فانشکن ویو را به این شکل ویرایش میکنیم:

```
def contact_us_page(request):
    if request.method == 'POST':
        contact_form = ContactUsForm(request.POST)
        if contact_form.is_valid():
            print(contact_form.cleaned_data)
            return redirect('home_page')
    else:
        contact_form = ContactUsForm()
```

متن فارسی خطای ظاهر شده برای این هست که در تنظیمات اصلی فایل ستینگ، لنگویج کد را روی فارسی قرار دادیم.

## قرار دادن تنظیمات برای فرم:

در خود فایل فرمز، ما میتوانیم برای هر کدام از فیلد هایمان، تنظیمات مورد نظر را قرار بدهیم، مثلا:

label: برای متن فیلد مورد نظر در تگ لیبل فیلد میباشد

max_length=50: برای فیلد مشخص میکند حداکثر تعداد کارکتر باید 50 باشد وگرنه اجازه ارسال به سمت سرور را نمیدهد

error_messages: یک دیکشنری میگیرد و برای هر خطایی میتوان متن خطای خودمان را بنویسیم

required: در نظر گرفتن اجباری یا اختیاری بودن فیلد که با ترو یا فالس مقدار میدهیم

```
full_name = forms.CharField(
    label='نام و نام خانوادگی',
    max_length=50,
    error_messages={
        'required': 'لطفا نام و نام خانوادگی خود را وارد کنید'
    })
```

widget: برای درنظر گرفتن نوع اینپوت میتونیم استفاده کنیم

`email = forms.EmailField(label='ایمیل', widget=forms.EmailInput)`
`text = forms.CharField(label='متن پیام', widget=forms.Textarea)`

