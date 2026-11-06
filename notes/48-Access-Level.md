# Access Level

باید برای ورود به پنل ادمین سطح دسترسی درنظر گرفته شود، برای این کار باید یک دکوریتور ایجاد کنیم؛ بطور کلی دکوریتور ها
این وظیفه را دارند که قبل از آن که بدنه یک متد اجرا شود، اول بررسی میکنند این بدنه قابلیت اجرا شدند را دارد یا خیر، یعنی
عملا میتوانیم اجرای یک متد را تحت کنترل خودمان در بیاریم؛ پس یکی از روش ها استفاده از دکوریتو است؛ مثلا ما میتوانیم در
متد خود چک کنیم اول کاربر لاگین باشد اگر لاگین بود دوباره چک کنیم که کاربر سوپریوزر باشد:

```
def index(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'admin_panel/home/index.html')
    return redirect(reverse('login_page'))
```

اما ما باید این ایف های تکراری را در هر فانکشن خود پیاده سازی کنیم که اصلا درست نیست؛ روش جایگزین و بهتر، استفاده از
دکوریتور ها است؛ در دکوریتور ما یک فانکشن داریم که ورودی یک فانکشن دیگر را میگیرد و داخل فانکشن یک فانکشن دیگر تعریف شده
مثل رپر، که رکوئست و آرگومان ها و کیوردآرگومان هایی که به فانشکن بیس ویو های دیگر ارسال شده است رو میگیرد و در نهایت
همان فانکشن رپر رو ریترن میکنیم. و برای استفاده از دکوریتور در بالای فانکشن بیس ویو ها از @ استفاده کرده و نام دکوریتور
را قرار میدهیم؛ پس بصورت کلی دکوریتور ما باتوجه به آن چیزی که میخواهیم به این شکل میشود است:

```
def permission_checker_decorator(func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('login_page'))

    return wrapper
```

و نحوه استفاده از آن :

```
@permission_checker_decorator
def index(request: HttpRequest):
    return render(request, 'admin_panel/home/index.html')
```

برای کلاس بیس ویو ها باید از متددکوریتور در بالای کلاس بیس ویو استفاده کرده و پارامتر اول دکوریتوری هست که باید به آن
پاس بدهیم:

```
@method_decorator(permission_checker_decorator, name='dispatch')
class ArticlesListView(ListView):
    model = Article
    paginate_by = 12
    template_name = 'admin_panel/articles/articles_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super(ArticlesListView, self).get_queryset()
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
        return query
```

## پیاده سازی سطح دسترسی شخصی خودمان:

میتوانیم سطح دسترسی را خودمان پیاده سازی کنیم، و این سطح دسترسی قرار هست به دکوریتور ارسال شود و چک شود آن یوزر به آن
پرمیشنی که ما برای دکوریتور درنظر گرفتیم رو دارد یا خیر؛ یعنی یوزر باید آن پرمیشن رو داشته باشد تا بتواند آن چیزی که ما
تعیین میکنیم رو مشاهده کند یا نکند؛ پس دکوریتور خود را به این صورت میتوانیم پیاده سازی کنیم:

```
def permission_checker_decorator_factory(data=None):
    def permission_checker_decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            print(data)
            if request.user.is_authenticated and request.user.is_superuser:
                return func(request, *args, **kwargs)
            else:
                return redirect(reverse('login_page'))

        return wrapper

    return permission_checker_decorator
```

در استفاده در فانکشن بیس ویو و کلاس بیس ویو ها :

```
@permission_checker_decorator_factory({'permission_name': 'admin_index'})
def index(request: HttpRequest):
    return render(request, 'admin_panel/home/index.html')
    


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class ArticlesListView(ListView):
    model = Article
    paginate_by = 12
    template_name = 'admin_panel/articles/articles_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super(ArticlesListView, self).get_queryset()
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
        return query
```

روش های مختلفی برای پیاده سازی سطوح دسترسی وجود دارد که هرکدام را خواسته باشیم میتوانیم استفاده کنیم.