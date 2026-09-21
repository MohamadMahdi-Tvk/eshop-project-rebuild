# List View

معمولا دو سناریو را در پروژه هایمان زیاد استفاده میکنیم، یکی نمایش لیست آیتم ها و دیگری نمایش جزئیات آیتم ها، در فریمورک
جنگو برای این دو سناریو، یکسری ویوهایی را ایجاد کرده است، یعنی عملا برای اینکه بیایم از تمپلیت ویو برای برگرداندن لیست
آیتم ها استفاده کنیم، میتونیم از لیست ویو استفاده کنیم و در کلاس از آن ارث بری انجام دهیم و تنها کاری لازم هست انجام
گیرد این هست که آدرس تمپلیت را به آن بدهیم و دوم آن مدل کلاس را معرفی کنیم و اگر داخل کلاس فانکشن گت را بنویسیم کلی متد
مختلف میاد که میتونیم آنها را اوراید کنیم:

```
class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
```

اما در تمپلیت، دیگر بعنوان پروداکت به آیتم ها دسترسی نداریم، بلکه توسط آبجکت لیست به آن دسترسی داریم:

```
{% for product in object_list %}
    {% include 'includes/product_item_partial.html' with product=product %}
{% endfor %}
```

اما میتونیم اسم آبجکت لیست هم در ویو تغییر بدیم تا با آن اسم در سمت تمپلیت به آن دسترسی داشته باشیم:

```
class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
```

در تمپلیت با نام پروداکتس به آن دسترسی خواهیم داشت:

```
{% for product in products %}
    {% include 'includes/product_item_partial.html' with product=product %}
{% endfor %}
```

## filter in ListView by get_queryset:

به راحتی میتوان در ویو فیلتر هم اعمال کرد تا دیتایی که مورد دلخواه ما هست نمایش داده شود مثلا اون آیتم هایی رو فقط
برگردان که فعال یا موجود باشند:

```
class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        base_query = super(ProductListView, self).get_queryset()
        data = base_query.filter(is_active=True)
        return data
```


