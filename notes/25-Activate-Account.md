# Activate Account

ما باید داخل اپلیکیشن خود، یک آدرسی درنظر بگیریم که که سگمنت سوم آن آدرس، همان رشته ای هست که به عنوان ایمیل اکتیوکد
درنظر گرفته ایم، زمانی که کاربر روی آن لینکی که به ایمیل او فرستاده شده، کلیک میکند، میاد در این آدرس و کد برای ما ارسال
میشود و ما این کد را دریافت کرده و با کدی که در دیتابیس هست چک میکنیم که آیا کاربری وجود دارد که ایمیل اکتیوکد آن با
چیزی که ارسال شده، یکی باشد یا خیر، اگر وجود داشت، حساب کاربری آن کاربر را فعال میکنیم و اگر نداشت، میبریمش در صفحه ی
ناتفاند؛ کل این پروسه منطق پیاده سازی فعالسازی حساب کاربری است.

`path('activate-account/<email_active_code>', views.ActivateAccountView.as_view(), name='activate_account')`

در ویو منطق رو پیاده سازی میکنیم:

```
class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                # todo: show success message to user
                return redirect(reverse('login_page'))
            else:
                # todo: show your account was activated message to user
                pass
            
        raise Http404
```

برای شبیه سازی ارسال ایمیل میریم داخل دیتابیس و برای یوزری که ثبت نام شده ایمیل اکتیوکدش را برداشته و به بصورت زیر در
یوآرال وارد میکنیم:

`http://127.0.0.1:8000/activate-account/3038cWSz16T7vgP3wcWWdygi4CYXAFp0AEBQciaS6tBgvpAeBhWpJQaaFTUwhkc3B6tQCt9N`

وقتی اینتر رو بزنیم، حساب کاربری فعال شده و ایزاکتیو برای کاربر ترو شده و همچنین یک کد جدید برای کاربر تولید میشود؛ در
واقعیت، لینک بالا را به ایمیل کاربر ارسال میکنیم و کاربر اگر رویش کلیک کرد، همین فرآیند طی شده و اکانتش فعال میشود.

