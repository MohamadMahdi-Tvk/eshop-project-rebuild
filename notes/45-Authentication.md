# Authentication

جالب نیست در هر متدی در ویو ابتدا با ایف چک کنیم اگر کاربر لاگین بود، آن ویو کار کند؛ سیستمی که خود جنگو بصورت اتوماتیک
برای ما فراهم کرده است، یک دکوریتو خیلی ساده و خوب هست؛ ویو های ما یا کلاس بیس ویو هستند، و یا فانکشن بیس ویو؛ پیاده
سازی برای این دو مورد متفاوت است.

## @login_required

کافیست بالای فانکشن بیس ویو های خود این دکوریتور را اضافه کنیم، در این صورت، کاربر حتما باید لاگین شده باشد تا به آن ویو
دسترسی داشته باشد:

```
from django.contrib.auth.decorators import login_required

@login_required
def user_basket(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return render(request, 'user_panel_module/user_basket.html', context)
```

برای این دکوریتو میتوانیم ورودی درنظر بگیریم که اگر کاربر لاگین نبود و خواست وارد این ویو شود، به کدام یوآرال برود، اگر
برایش ورودی درنظر نگیریم، بطور پیش فرض آدرس اکانت/لاگین برایش ست شده است:

```
http://127.0.0.1:8000/accounts/login/?next=/user/user-basket
```

برای اینکه آدرس را خودمان مشخص کنیم، باید داخل ورودی دکوریتور اسم لاگین را برایش مشخص کینم:

`@login_required(login_url='login_page')`

برای اینکه مدام نیایم اسم آدرس را به دکوریتور بدهیم، بهتر هست بیایم و در فایل ستینگز پروژه آدرس یوآرال را برای کل پروژه
مشخص کنیم؛ این روش بهتر هست، چون که اگر آدرس لاگین عوض شد، مجبور نباشیم همه جا آن ها را عوض کنیم؛ پس در فایل ستینگز:

`LOGIN_URL = '/login'`

## dispatch ()

این فانکشن در کلاس بیس ویو ها وجود دارد؛ این متد در پس زمینه بوسیله کلاس بیس ویو ها فراخوانی میشود و این متد مشخص میکند
که الان باید کدامیک از درخواست ها پردازش شود و یکسری کار ها را میتواند مدیرین کند، بطور مثال در یک کلاس بیس ویویی که متد
های گت و پست دارد، فانکشن دیسپچ مشخص میکند که کدامیک از این متد ها باید اجرا شود، پس میتوانیم این را تحت اختیار خود قرار
دهیم و آن چیزی که میخواهیم را پیاده سازی کنیم:

```
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'

    def dispatch(self, request, *args, **kwargs):
        pass
```

برای اینکه بتوانیم برای یک کلاس بیس ویو از لاگین ریکوآیرد استفاده کنیم، باید متد دکوریتور را ایمپورت کنیم:

`from django.utils.decorators import method_decorator`

حالا در بالای کلاس بیس ویو باید از متد دکوریتور استفاده کنیم و دکوریتور لاگین ریکوآیرد رو در ورودی اول بهش میدهیم، ورودی
دوم یک نیم از ما میخواهد، یعنی میپرسه کدام متد منظورماست که متد دیسپچ رو بهش پاس میدیم؛ اتفاقی که میفته اینه که زمانی که
درخواست وارد کلاس بیس ویوی ما میشود، اولین چیزی که اجرا میشود، فانکشن دیسپچ هست، ما برای همین فانکشن اگر لاگین ریکوایرد
رو اعمال کنیم، اگر کاربر لاگین نباشد، بقیه دستورات اجرا نمیشوند. لازم نیست متد دیسپچ رو در کلاس بیس ویوی خود بنویسیم:

```
@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'
```