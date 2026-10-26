# Dynamic Product Slider

در بعضی جاهای صفحه ی سایت ما یک لیست 4 تایی از محصولات را به کاربر نمایش میدهیم، مثلا قسمتی داریم به اسم پرفروش ترین
محصولات که یک لیست با 4 تا محصول هست، یعنی در یک لیست 3 تا لیست دیگر باید وجود داشته باشد؛ منطق پیاده سازی لیستی که 3 تا
لیست 4 آیتمی داخلش هست به این شکل است:

```
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
res_list = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

grouped_list = []
group_size = 2

my_range = range(0, len(my_list), group_size)
print(list(my_range))

for i in my_range:
    grouped_list.append(my_list[i:i + group_size])
   
print(grouped_list)
```

اما برای پیاده سازی میتوانیم، منطق را در یک ماژول دیگر که مربوط به فانکشن های کلی پروژه هست و یک فانکشن پیاده سازی کنیم
و هرجایی از پروژه لازم بود از آن استفاده کنیم:

```
def group_list(custom_list, size=4):
    grouped_list = []
    for i in range(0, len(custom_list), size):
        grouped_list.append(custom_list[i:i + size])
    return grouped_list
```

در ویو میایم براساس آیدی مرتب میکنیم و 12 تا آیتم را واکشی میکنیم و به فانشکنی که ساخته ایم پاس میدهیم:

```
class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sliders = Slider.objects.filter(is_active=True)
        context['sliders'] = sliders
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
        context['latest_products'] = group_list(latest_products)
        return context
```

حال میتوان در تمپلیت از کانتکس استفاده کرد:

```
{% for group in latest_products %}
    <div class="item {% if forloop.first %} active {% endif %}">
         {% for product in group %}
             <div class="col-sm-3">
                 <div class="product-image-wrapper">
                     <div class="single-products">
                         <div class="productinfo text-center">
                             <img src="{{ product.image.url }}" alt=""/>
                             <h2>{{ product.price }}</h2>
                             <p>{{ product.title }}</p>
                             <a href="#" class="btn btn-default add-to-cart"><i
                                     class="fa fa-shopping-cart"></i>افزودن به سبـد خرید</a>
                         </div>
                     </div>
                 </div>
             </div>
         {% endfor %}
    </div>
{% endfor %}
```
