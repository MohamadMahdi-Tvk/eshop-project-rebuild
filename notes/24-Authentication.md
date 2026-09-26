# Authentication

## Register

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

