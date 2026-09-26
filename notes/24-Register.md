# Register

در متد گت که یک فرم ثبت نامی رو به کاربر نمایش میدهیم، اما منطق ثبت نام کاربر در متد پست اتفاق میفتد، یعنی در پست چک
میکنیم اگر فرم معتبر بود، باید یکسری پردازش هایی صورت بگیرد و عملیات ثبت نام کاربر انجام شود، در فرمز هم میتونیم یکسری
اعتبارسنجی برای ثبت نام کاربر درنظر بگیریم.

ما میتونیم ولیدیتور های دلخواه خودمان را بسازیم، داخل فرم ها، اگر فانشکن و کلمه کلیدی دف رو بزنیم و کلین رو تایپ کنیم،
یکسری متد هایی رو مشاهده میکنیم که میتونیم اعتبارسنجی های خودمان را پیاده سازی کنیم؛ مثلا میخواهیم ورود مجدد رمز عبور را
اعتبارسنجی کنیم و مقایسه کنیم که آیا رمز اول با رمز دوم برابر هست یا خیر؛ یا مثلا میخواهیم افرادی که اکانت یاهو دارند را
از ثبت نام جلوگیری کنیم و برای ایمیل هم میتونیم اعتبارسنجی پیاده سازی کنیم:

```
class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator()
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput()
    )

    def clean_email(self):
        pass

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')
```

قدم اول برای ثبت نام کاربر، باید بریم سراغ مدل یوزر که داخل ماژول اکانت قرار گرفته است و آن را در ویوز ایمپورت میکنیم تا
بتوانیم با آن ثبت نام را انجام دهیم و بررسی های لازم رو مثل تکراری نبودن آدرس ایمیل در اینجا انجام میدهیم.

## email__iexact:

چک میکند ایمیلی که بهش میدهیم مقدارش دقیقا با ایمیلی که در دیتابیس هست برابر هست یا خیر.

## email_active_code:

این فیلدی که درنظر گرفته ایم برای سیستم فعالسازی حساب کاربری فرد هست، یعنی ما باید مطمئن شویم ایمیلی که کاربر وارد کرده،
ایمیل درستی هست، در اینجا میایم یک کد فعالسازی تولید میکنیم که میشه همین ایمیل اکتیو کد، و میایم همین اکتیوکد را در قالب
یک لینک، برای ایمیل آن کاربر ارسال میکنیم و اگر کاربر روی آن لینک کلیک کند، سیستم تشخیص میدهد که کاربر واقعا ایمیل درستی
وارد کرده است و ما هم حساب کاربر را فعال میکنیم و تا زمانی هم که حساب کاربر فعال نشده، نمیتواند لاگین کند. اگر هم براساس
موبایل باشد، ساختارش دقیقا به همین روال است.

## register in views.py:

```
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__exact=user_email).exists()
            if user:
                register_form.add_error('email', 'ایمیل وارد شده تکرار میباشد')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=user_email
                )
                new_user.set_password(user_password)
                new_user.save()

                # todo: send email active code

                return redirect(reverse('login_page'))

        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)


class LoginView(View):
    def get(self, request):
        context = {
            'login_form': None
        }
        return render(request, 'account_module/register.html', context)

    def post(self, request):
        pass

```

