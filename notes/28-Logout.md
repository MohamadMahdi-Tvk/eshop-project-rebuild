# Logout

برای خارج شدن از حساب کاربری هم باید یک ویو بسازیم:

```
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))
```

آدرس آن هم ایجاد میکنیم:

```
path('logout/', views.LogoutView.as_view(), name='logout_page'),
```

# Send Email Template:

داخل فولدر تمپلیتسی که در روت پروژه هست یک فولدر به اسم ایمیل میسازیم و یک فایل اچتی ام ال با نام اکتیو_اکانت داخلش
اکانت میسازیم و اینجا باید تمپلیتی که قرار هست به کاربر ارسال شود رو درست کنیم؛ معمولا تگ های اصلی اچتی ام ال رو استفاده
نمیکنیم و فقط تگ های مورد نیاز رو قرار میدهیم:

```
<div dir="rtl">
    <h2>فعالسازی حساب کاربری</h2>
    <hr>
    <p>کاربر گرامی، جهت فعالسازی حساب کاربری خود، روی لینک زیر کلیک کنید</p>
    <p>
        <a href="http://localhost:8000{% url 'activate_account' email_active_code=user.email_active_code %}">فعالسازی حساب کاربری</a>
    </p>
</div>
```

برای ارسال ایمیل میتونیم از تمپلیت های آماده ای که در اینترنت هست هم استفاده کنیم.

برای مبحث فراموشی کلمه عبور هم باید یک تمپلیت جدا ایجاد کنیم:

```
<div dir="rtl">
    <h2>بازیابی کلمه عبور</h2>
    <hr>
    <p>کاربر گرامی، جهت بازیابی کلمه عبور حساب کاربری خود، روی لینک زیر کلیک کنید</p>
    <p>
        <a href="http://localhost:8000{% url 'reset_password_page' active_code=user.email_active_code %}">بازیابی کلمه عبور</a>
    </p>
</div>
```