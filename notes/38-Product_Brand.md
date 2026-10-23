# Product Brand

## annotate:

یکی از قابلیت های جنگو کوئری ست هست، دستور انوتیت، روی آبجکت اعمال میشود و میگه دیتایی که میخوای رو واکشی کن، چیز های
اضافی که نیاز داری من برات میارم، دستور انوتیت و دستور اگریگیت، جفتشون برای موارد اضافی هستند، فقط انوتیت روی هر سطر
اعمال می کند، یعنی فرضا اگر هزار تا آیتم داریم، انوتیت روی هر هزار تا اعمال می شود، در اینجا، به ازای هر آیتمی که داخل
پروداکت برند واکشی میشود، میره و تعداد محصول هر برند رو هم در اون دیتای واکشی شده، اضافه میکند:

```
def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brands
    }
    return render(request, 'product_module/components/product_brands_component.html', context)
```