# Product Visit

وقتی به صفحه ی جزئیات هر محصولی میرویم باید یک بازدید برای آی پی ما ثبت گردد و در نهایت تعداد بازدید هر محصول را براساس
دیتایی که در جدول ویزیت ادد کرده ایم، محاسبه میکنیم. ما در این مدل یک آی پی ثبت میکنیم، و اگر هم کاربری لاگین بود،
میخوایم بدانیم کدام کاربر آن محصول را دیده است، پس با یوزر هم ارتباط دارد:

```
class ProductVisit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='کاربر', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید های محصول'
```

## META

رکوئست، یک آیتمی درون خودش دارد به اسم متا، از داخل آن میتوانیم یک کلیدی را گت کنیم و آیپی آن شخصی که وارد شده را بر
میگرداند؛ میتوانیم از یکی از این دو مورد استفاده کنیم:

```
class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sliders = Slider.objects.filter(is_active=True)
        context['sliders'] = sliders
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
        context['latest_products'] = group_list(latest_products)

        request: HttpRequest = self.request
        print(request.META.get('HTTP_X_FORWARDED_FOR')) # None
        print(request.META.get('REMOTE_ADDR')) # 127.0.0.1 چون آیپی ما لوکال هست این رو نمایش میدهد

        return context
```

پس میتوانیم آن را در متدی جداگانه ایجاد کنیم و از آن در جاهای دیگر استفاده کنیم:

```
from django.http import HttpRequest

def get_client_ip(request: HttpRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

```

حال در جایی که میخواهیم میتوانیم از آن استفاده کنیم، مثلا وارد جزئیات هر محصول که شدیم باید یک بازدید برای آن محصول ثبت
شود:

```
class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        favorite_product_id = request.session.get('product_favorite')
        context['is_favorite'] = favorite_product_id == str(loaded_product.id)
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPositions.product_detail)
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()
        return context
```

حال میتوان در صفحه ویو، پربازدیدترین محصولات را نمایش دهیم.