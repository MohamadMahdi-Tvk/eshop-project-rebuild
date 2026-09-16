# Django Forms Save

## ایجاد فرم و اینپوت ها با استفاده از فور:

میتوان بجای آنکه تک تک بیایم موارد مربوط به اینپوت را در صفحه قرار بدیم، میتونیم با ایف این کار را انجام دهیم البته اگر
خواسته باشیم یکسری تنظیمات خاص مثل ایف برای اینپوت ها قرار دهیم، باید از روش قبل استفاده کنیم ولی اگر دوست داشتیم
میتونیم از این روش زیر هم استفاده کنیم و فرقی ندارد.

```
{% for field in contact_form %}
    <div class="col-md-12 form-group">
        {{ field.label_tag }}
        {{ field }}
        {{ field.errors }}
    </div>
{% endfor %}
```

## ذخیره سازی اطلاعات داخل فرم:

باید از مدل یک نمونه جدید ایجاد شود و اطلاعات را با استفاده از مقادیر که در فرم تعریف کردیم پر کنیم و سپس ذخیره کنیم:

```
def contact_us_page(request):
    if request.method == 'POST':
        contact_form = ContactUsForm(request.POST)
        if contact_form.is_valid():
            print(contact_form.cleaned_data)
            contact = ContactUs(
                title=contact_form.cleaned_data.get('title'),
                full_name=contact_form.cleaned_data.get('full_name'),
                email=contact_form.cleaned_data.get('email'),
                message=contact_form.cleaned_data.get('message')
            )
            contact.save()
            return redirect('home_page')
    else:
        contact_form = ContactUsForm()

    return render(request, 'contact_module/contact_us_page.html', {
        'contact_form': contact_form
    })
```

## ModelForm:

ما تا الان اومدیم در فایل فرمز، یکسری پراپرتی ایجاد کردیم و برایش مشخصاتی تعیین کردیم؛ اما میتوان با استفاده از مدل فرم
بیایم و به جنگو بگیم مستقیما از خود مدل ما برای ایجاد فرم استفاده کند؛ پس فرم ما مستقیما متصل میشود به خود دیتابیس و
دیگر لازم نیست خودمان کار خاصی انجام بدهیم:

```
class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'title', 'message']
```

### model:

مدل خود را برای فرم مشخص میکنیم.

### fields:

فیلد هایی که قرار هست نمایش داده شود یا پر شود رو برای مدل فرم در قالب یک لیست با نام همان فیلد های کلاس مدل مشخص
میکنیم؛ یعنی میگیم این فرم ما برای این فیلد هایی که مشخص میکنیم جنریت شود. اگر هم همه فیلد ها مد نظر بود، میتونیم
بنویسیم:

`fields = '__all__'`

### exclude

برایش مشخص میکنیم چه فیلد هایی رو نمیخواهیم در تولید فرم جنریت شوند مثلا:

`exclude = ['response']`

بعد از آن به ویو رفته و تغییرات لازم را میدهیم و این بار از مدل فرمی که ساخته ایم استفاده میکنیم:

```
def contact_us_page(request):
    if request.method == 'POST':
        contact_form = ContactUsModelForm(request.POST)
        if contact_form.is_valid():
            print(contact_form.cleaned_data)
            contact = ContactUs(
                title=contact_form.cleaned_data.get('title'),
                full_name=contact_form.cleaned_data.get('full_name'),
                email=contact_form.cleaned_data.get('email'),
                message=contact_form.cleaned_data.get('message')
            )
            contact.save()
            return redirect('home_page')
    else:
        contact_form = ContactUsModelForm()

    return render(request, 'contact_module/contact_us_page.html', {
        'contact_form': contact_form
    })

```







