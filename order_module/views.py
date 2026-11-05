import time
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from product_module.models import Product
from .models import Order, OrderDetail
from django.conf import settings
import requests

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


@login_required
def verify_payment(request):
    current_order, created = Order.objects.get_or_create(
        is_paid=False,
        user_id=request.user.id
    )
    total_price = current_order.calculate_total_price()

    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    if status != 'OK' or not authority:
        # return HttpResponse("پرداخت توسط کاربر لغو شد.")
        return render(request, 'order_module/payment_result.html', {
            'cancel': 'پرداخت توسط کاربر لغو شد'
        })

    # مبلغ باید دقیقاً همان مبلغ درخواست اولیه باشد.
    # فعلاً این مقدار را از سفارش ذخیره‌شده دریافت کن.
    payment_amount = total_price * 10

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
                current_order.is_paid = True
                current_order.payment_date = time.time()
                current_order.save()

                ref_id = result['data']['ref_id']

                # اینجا سفارش را پرداخت‌شده کن
                # و ref_id را در دیتابیس ذخیره کن.

                # return HttpResponse(
                #     f"پرداخت موفق بود. کد پیگیری: {ref_id}"
                # )
                return render(request, 'order_module/payment_result.html', {
                    'success': f'تراکنش شما با کد پیگیری {ref_id} باموفقیت انجام شد'
                })

            # return HttpResponse(
            #     f"پرداخت تأیید نشد: {result.get('errors')}"
            # )
            return render(request, 'order_module/payment_result.html', {
                'info': 'پرداخت تایید نشد'
            })

        # return HttpResponse(
        #     f"خطا در تأیید پرداخت: {result}",
        #     status=502
        # )
        return render(request, 'order_module/payment_result.html', {
            'error': 'خطا در تایید پرداخت'
        })

    except requests.exceptions.RequestException as e:
        # return HttpResponse(f"خطای ارتباطی: {e}", status=502)
        return render(request, 'order_module/payment_result.html', {
            'connection_error': f'خطای ارتباطی: {e}'
        })
