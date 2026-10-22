# Edit User

## initial:

ما وقتی نمونه ای از فرم در ویوی خود ایجاد میکنیم میتونیم بهش ورودی اینیشیال را پاس بدیم، که یک دیکشنری هست و میتونیم
برای کلید های مختلف که همان فیلد های فرم میشوند، مقدار اولیه ای ست کنیم، مثلا:

```
class EditUserProfilePage(View):
    def get(self, request: HttpRequest):
        edit_form = EditProfileModelForm(initial={
            'first_name': 'علیرضا',
            'last_name': 'کریمی',
            'address': 'تهران'

        })
        context = {
            'form': edit_form
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)
```

اما باید اطلاعات کاربری که هم اکنون لاگین هست رو پر کنیم؛ باید به این صورت عمل کنیم:

```
class EditUserProfilePage(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(initial={
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'address': current_user.address

        })
        context = {
            'form': edit_form
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)
```

## instance:

ما بجای اینیشیال، میتونیم از اینتنس استفاده کنیم که راهکار بهتری است و اگر بخواهیم فرمی برای ویرایش شود، باید از اینتنس
استفاده کنیم، یعنی میایم و اینتسنس مربوط به ویرایش آن آیتم را باید بهش بدیم و بهش میگیم مقدار اینستنس آن همان کاربر فعلی
است و چون مدل فرم هست باید اینستنس همان مدلی را داشته باشد که ما داخل کلاس فرمز خود تعریف کرده ایم، یعنی مدل ما حتما
باید از نوع یوزر باشد:

```
class EditUserProfilePage(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)
        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)
```

نکته درمورد ایمپورت اتوماتیک یک ماژول:
در کپی پیست های کد ها یک زمان هایی ممکن هست ماژولی استفاده شده باشد که در بالای کد ها ایمپورت نشده باشد، با نگه داشتن
موس روی آن کد که خط قرمز زیرش قرار گرفته و زدن دکمه های آلت و اینتر یک کادر باز میشود که روی گزینه ایمپورت دیس نیم کلیک
کرده و میتونیم فایل مورد نظر را در صفحه خود ایمپورت کنیم.