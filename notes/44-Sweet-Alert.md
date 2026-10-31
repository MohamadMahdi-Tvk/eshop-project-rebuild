# Sweet Alert

پکیج های جاوا اسکریپتی زیادی برای نمایش اعلان ها و پیغام ها به کاربر وجود دارد و میتوانیم از هر کدام که خواستیم استفاده
کنیم، یکی از معروف ترین ها سوئیت آلرت هست؛ آدرس سایت آن:

`https://sweetalert2.github.io/`

میتوانیم از سی دی ان آن استفاده کنیم، پس آن را در فوتر رفرنسز های پروژه خود اضافه میکنیم و حتما باید قبل از کاستوم جی اس
خودمان باشد:

`<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>`

یکی از نمونه هایی که در سایت هست رو به فایل کاستوم جی اس خودمان منتقل میکنیم و در جایی که میخواهیم از آن استفاده میکنیم
و باتوجه به آن چیزی که خودمان میخواهیم تغییرات را مد نظر را انجام میدهیم:

```
function addProductToOrder(productId) {
    const productCount = $('#product-count').val();
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount).then(res => {
        Swal.fire({
            title: "اعلان",
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            confirmButtonText: res.confirm_button_text
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '/login'
            }
        });
    });
}
```

در فانکشن ویو:

```
def add_product_to_order(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'مقدار وارد شده معتبر نمی باشد',
            'confirm_button_text': 'مرسی از شما',
            'icon': 'warning'
        })

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()
            else:
                new_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_detail.save()

            return JsonResponse({
                'status': 'success',
                'text': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد',
                'confirm_button_text': 'باشه ممنونم',
                'icon': 'success'
            })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول مورد نظر یافت نشد',
                'confirm_button_text': 'مرسی از شما',
                'icon': 'error'
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزودن محصول به سبد خرید ابتدا می بایست وارد سایت شوید',
            'confirm_button_text': 'ورود به سایت',
            'icon': 'error'
        })
```