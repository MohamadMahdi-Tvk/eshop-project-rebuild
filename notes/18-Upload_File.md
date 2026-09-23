# Upload File

میایم اول آپلود فایل در پایتون در بررسی میکنیم:

```
def store_file(file):
    with open('temp/image.jpg', "wb+") as dest:
        for chunk in file.chunks():
            dest.write(chunk)
```

در ساختار آپلود فایل ها، اگر حجم فایل آپلودی زیاد شود، مثلا 200 مگابایت به بالا، اگر بیایم از دستور رید روی فایل استفاده
کنیم، یعنی یکدفعه کل آن آیتم رو بخوانیم، مموری زیادی درگیر خواهد شد، در تعداد درخواست های پایین مشکلی ایجاد نمیشود، ولی
زمانی که تعداد کاربران آنلاین زیاد میشوند، قطعا به مشکل میخورد، پس ما میایم آن را بصورت چانک فایل درنظر میگیریم، یعنی
زمانی که فایل داره آپلود میشود، تکه تکه فایل ها را دریافت میکند و تکه تکه کنار هم قرار میدهد و یک فایل واحد را ایجاد
میکند و آنرا ذخیره میکند؛ یک فولدر تمپ هم داخل روت اصلی پروژه میسازیم که بتواند در آنجا ذخیره کند که اگر این کار را
نکنیم ارور میگیریم؛ حالا در ادامه زمانی که فایل آپلود میشود آنرا دریافت میکنیم:

```
class CreateProfileView(View):
    def get(self, request):
        return render(request, 'contact_module/create_profile_page.html')

    def post(self, request):
        store_file(request.FILES['profile'])
        return redirect('/contact-us/create-profile')
```

در فایل تمپلیت و در تگ فرم:

```
<form id="main-contact-form" class="contact-form row" action="{% url 'create_profile_page' %}" method="post" enctype="multipart/form-data">
{% csrf_token %}

<input type="file" name="profile">

<div class="form-group col-md-12">
    <button type="submit" class="btn btn-primary pull-right">ارسال</button>
</div>
</form>
```

الان اگر عکس را آپلود کنیم، داخل پوشه تمپ ذخیره میشود.

## دستورات بهتر برای آپلود

ما میتونیم فرم آن هم بسازیم؛ یعنی در فایل فرمز، میتونیم یک کلاس درنظر بگیریم که از فرمز.فرم ارث بری کند و برای فایل،
فیلد از نوع فایل فیلد درنظر بگیریم:

```
class ProfileForm(forms.Form):
    user_image = forms.FileField()
```

میریم و در ویو از فرم استفاده میکنیم:

```
class CreateProfileView(View):
    def get(self, request):
        form = ProfileForm()
        return render(request, 'contact_module/create_profile_page.html', {
            'form': form,
        })

    def post(self, request):
        store_file(request.FILES['profile'])
        return redirect('/contact-us/create-profile')
```

سپس در فایل تمپلیت هم درست میکنیم:

```
<form id="main-contact-form" class="contact-form row" action="{% url 'create_profile_page' %}" method="post" enctype="multipart/form-data">
    {% csrf_token %}

    {{ form }}

 <div class="form-group col-md-12">
     <button type="submit" class="btn btn-primary pull-right">ارسال</button>
 </div>
</form>
```

و در ویو هم تغییرات زیر را اعمال میکنیم:

```
class CreateProfileView(View):
    def get(self, request):
        form = ProfileForm()
        return render(request, 'contact_module/create_profile_page.html', {
            'form': form,
        })

    def post(self, request):
        submitted_form = ProfileForm(request.POST, request.FILES)
        if submitted_form.is_valid():
            profile = UserProfile(image=request.FILES['user_image'])
            profile.save()
            return redirect('/contact-us/create-profile')

        return render(request, 'contact_module/create_profile_page.html', {
            'form': submitted_form,
        })
```

ما یک مدل هم بسازیم که یک فایل داخلش ذخیره شود؛ یک کلاس مدل تستی ایجاد میکنیم صرفا برای یادگیری مبحث آپلود فایل؛ نکته
مهم این هست که برای ذخیره سازی فایل ها در سرور، نمیایم خود اون فایل را مستقیما در دیتابیس ذخیره کنیم، این یکی از بدترین
کارهای ممکن هست و منطقی نیست؛ کاری که میکنن این هست که خود فایل را در یک مکان فیزیکی ذخیره میکنند و در دیتابیس میان آدرس
آن فایل را ذخیره و نگهداری میکنند. در کلاس مدل میتونیم از فایل فیلد برای دریافت فایل استفاده کرد و یک پارامتر ورودی داخل
آن هست به اسم آپلودتو، که مسیر آپلود آن فایل را برایش مشخص میکنیم؛ اما برای آنکه مسیر مشخصی برای فایل درنظر بگیریم باید
بریم داخل ستینگ و مدیا روت تعریف کنیم؛ این مورد مشخص میکند که این فایل هایی که توسط کاربران آپلود میشوند، بصورت پیش فرض
کجا ذخیره شوند؛ و در فیلد کلاس مدل در آپلودتو، هر اسمی قرار بدهیم، میشود یک زیر فولدر برای آن فولدری که در ستینگ تنظیم
کردیم؛ پس باید مدیا روت رو طوری درنظر بگیریم که اگر زمانی پروژه در سرور قرار گرفت، اون مسیر فیزیکی طی شود و به مسیر
پروژه برسد و یک پوشه ای درنظر گرفته شود که فایل ها داخل آن پوشه قرار بگیرند؛ برای اینکار میگیم بره سراغ آدرس پیش فرض
پروژه و سپس / و اسم اون فولدری که مد نظر ماست و آن فولدر هم در روت میسازیم:

`MEDIA_ROOT = BASE_DIR / 'uploads'`

کلاس مدل:

```
class UserProfile(models.Model):
    image = models.FileField(upload_to='images')
```

سپس مایگریشن زده تا تغییرات اعمال شود و سپس پروژه را تست میکنیم. اگر بار دوم یک عکسی که بار اول آپلود کردیم، آپلود کنیم،
جنگو برای اینکه نام تکراری ذخیره نکند، یک متن رندوم در آخر اسم عکس برایش درنظر میگیرد؛ پس حذف فایل نداریم.


