# Zarin Pal

یکی از روش های پیاده سازی درگاه پرداخت، زرین پال می باشد، هر درگاه پرداختی یکسری مستندات و نمونه کد هایی دارد که ما باید
ابتدا آن مستنداتی که در سایت گفته شده را مطالعه کرده و سپس طبق آن، درگاه پرداخت پروژه خود را پیاده سازی کنیم.

`https://www.zarinpal.com/docs/`

ابتدا باید پکیج زیر را نصب کنیم:

`pip install requests`

اگر نمونه کد را که در گیت هاب هست، مشاهده کنیم، یک فایل یوآرالز میدهد و یک فایل ویوز؛ در فایل یوآرالز، دوتا آدرس درنظر
گرفته شده است؛ پس دوتا آدرس رو باید در سورس کد داشته باشیم؛ یکی رکوئست هست و یکی وریفای، آدرس رکوئست، اون درخواست ما
برای پرداخت یک مبلغی رو ارسال میکند سمت سرور زرین پال و اگر همه چی اوکی بود، وارد درگاه پرداخت میشویم، زمانی که از درگاه
پرداخت برمیگردیم، دوباره باید یک تاییدیه از درگاه پرداخت دریافت کنیم که پرداخت واقعا انجام شده یا خیر، پس چه پرداخت
انجام شود چه نشود، کاربر به سایت باز میگردد، آدرس وریفای به عنوان بررسی نتیجه پرداخت کاربر به زرین پال میفرستیم، که
زمانی که زرین پال کارش تمام شد، کاربر را به اون آدرسی که بهش دادیم برگرداند، که ما در این آدرس دوباره از زرین پال
میپرسیم که کاربر خریدش را باموفقیت انجام داده یا خیر و منطق خود را پیاده سازی میکنیم:

```
from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify , name='verify'),
]
```

یک فایل ویوز هم دارد که ساختار اصلی درگاه پرداخت هست؛ کد ها آن را در ماژول مربوط به اوردر پیاده سازی میکنیم. یکسری
اطلاعات هستند که باید به زرین پال ارسال شوند یعنی:

```
#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/order/verify-payment/'
```

این دو را هم در فایل ستینگز اضافه میکنیم:

```
MERCHANT = "00000000-0000-0000-0000-000000000000"
SANDBOX = True
```

توضیحات :

1. MERCHANT : همان کلیدی هست که درگاه پرداخت زرین پال، پس از آنکه در سایتش ثبت نام کردیم و احراز هویت شدیم در اختیار ما
   قرار میدهد.
2. ZP_API_... : زمانی که بخواهیم کاربر رو به سمت درگاه پرداخت ارسال کنیم یا برگردانیم از آن ها استفاده میکنیم؛ پس برای
   مباحث انتقال دیتا کاربرد دارند.
3. amount : مقدار مبلغ به ریال
4. description : توضیحات که اجباری است
5. email & mobile : این موارد اجباری نیستند
6. CallbackURL : برای اینکه مشخص کند زمانی که تراکنش کاربر ثبت شد و پرداختش نهایی شد، به کدام آدرس برگردانده شود و
   اطلاعات پرداختی رو به کی بده که باید ساختاری که خودمان ساختیم رو بهش پاس بدیم.
7. در متد رکوئست پیمنت از این اطلاعات استفاده میکنیم و دیتاها را به درگاه ارسال میکنیم
8. متد وریفای پیمنت هم طبق کد هایی که داریم پیاده سازی میکنیم، که برای بعد از عملیات پرداخت است

نکته مهم:
همیشه باید آخرین مستنداتی که درگاه پرداخت ها ارائه میدهند پیش برویم، بطور مثال در آموزش از نسخه قدیمی استفاده شده بود،
که موقع پیاده سازی کار نکرد، اما وقتی طبق آخرین مستندات پیاده سازی کردیم، صفحه درگاه پرداخت به درستی نمایش داده شد:

```
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
amount = 1000
description = "نهایی کردن کردن خرید شما از سایت ما"
phone = ''
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'

@login_required
def request_payment(request: HttpRequest):

    current_order, created = Order.objects.get_or_create(
        is_paid=False,
        user_id=request.user.id
    )

    total_price = current_order.calculate_total_price()

    if total_price <= 0:
        return redirect('user_basket_page')

    data = {
        "merchant_id": settings.MERCHANT,
        "amount": total_price * 10,
        "description": description,
        "callback_url": CallbackURL,
    }

    try:
        response = requests.post(
            ZP_API_REQUEST,
            json=data,
            timeout=15
        )

        result = response.json()

        print("Zarinpal Status:", response.status_code)
        print("Zarinpal Response:", result)

        if response.status_code == 200:

            if result.get('data', {}).get('code') == 100:

                authority = result['data']['authority']

                return redirect(
                    ZP_API_STARTPAY + authority
                )

            return HttpResponse(
                f"خطای زرین‌پال: {result.get('errors')}",
                status=502
            )

        return HttpResponse(
            f"HTTP Error: {response.status_code} - {result}",
            status=502
        )

    except requests.exceptions.Timeout:
        return HttpResponse("اتمام زمان اتصال به زرین‌پال", status=504)

    except requests.exceptions.ConnectionError:
        return HttpResponse("خطا در اتصال به زرین‌پال", status=502)

    except (ValueError, KeyError) as e:
        return HttpResponse(f"خطای پردازش پاسخ: {e}", status=502)


def verify_payment(request):

    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    if status != 'OK' or not authority:
        return HttpResponse("پرداخت توسط کاربر لغو شد.")

    # مبلغ باید دقیقاً همان مبلغ درخواست اولیه باشد.
    # فعلاً این مقدار را از سفارش ذخیره‌شده دریافت کن.
    payment_amount = ...

    data = {
        "merchant_id": settings.MERCHANT,
        "amount": payment_amount,
        "authority": authority,
    }

    try:
        response = requests.post(
            ZP_API_VERIFY,
            json=data,
            timeout=15
        )

        result = response.json()

        if response.status_code == 200:

            if result.get('data', {}).get('code') == 100:
                ref_id = result['data']['ref_id']

                # اینجا سفارش را پرداخت‌شده کن
                # و ref_id را در دیتابیس ذخیره کن.

                return HttpResponse(
                    f"پرداخت موفق بود. کد پیگیری: {ref_id}"
                )

            return HttpResponse(
                f"پرداخت تأیید نشد: {result.get('errors')}"
            )

        return HttpResponse(
            f"خطا در تأیید پرداخت: {result}",
            status=502
        )

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"خطای ارتباطی: {e}", status=502)
```

## Project Packages:

برای اینکه لیست پکیج های نصب شده را مشاهده کنیم، دستور زیر را در ترمینال میزنیم:

`pip freeze`

