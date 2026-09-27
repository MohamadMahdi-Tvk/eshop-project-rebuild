# login

در فرم ورود به پنل ادمین، در منطق برنامه چک میشود که کاربر حتما باید در دیتابیس، فیلد ایزسوپریوز او ترو باشد تا بتواند
وارد پنل ادمین شود، اما ما فرمی جداگانه برای کاربران معمولی پیاده سازی میکنیم که از سایت استفاده کنند.

در ابتدا باید موارد لازم را چک کنیم که آیا کاربر فعال هست یا نه یا اینکه آیا ایمیل و پسوردش درست هست یا خیر، بعد از این
کارها، کاربر باید لاگین شود، برای لاگین کردن هم باید کوکی ست شود؛ ما وقتی در پنل ادمین لاگین میکنیم، اگر تب اپلیکیشن در
مرورگر رو مشاهده کنیم، برای ما یک سشن آیدی اضافه میشود، این سشن آیدی میشه اطلاعات هویتی ما زمانی که میخواهیم لاگین کنیم؛
پس این سشن آیدی اطلاعات مارا داخل خودش نگهداری میکند و زمانی که بخواهیم صفحه ای را باز کنیم، این کوکی، در هد هر درخواست،
ارسال میشود؛ یعنی اگر در تب نتورک باشیم و قسمت هدرز برویم، میتونیم سشن آیدی همراه با مقدارش رو مشاهده کنیم، یعنی با
هربار رفرش این سشن آیدی در هد درخواست ارسال میشود و اگر بریم در کوکی ها و اون سشن آیدی رو پاک کنیم، دیگه به ادمین دسترسی
نخواهیم داشت و دیگر لاگین نیست. برای اینکه این سیستم رو داخل فرم های لاگین خودمان پیاده سازی کنیم کافیست ماژول های لاگین
و لاگوت را ایمپورت کنیم و از آنها برای لاگین در قسمت پست ویو استفاده کنیم؛ با فراخوانی کردن همین لاگین، خودش میاد کاربر
رو لاگین میکند، کوکی را ست کرده و همه ی موارد رو خودش انجام میدهد:

```
from django.contrib.auth import login, logout

class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده است')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('email', 'نام کاربری یا کلمه عبور اشتباه است')
            else:
                login_form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)
```