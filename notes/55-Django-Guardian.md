# Django Guardian

با این پکیج، امکان بررسی سطوج دسترسی براساس آبجکت هم داریم، طریقه نصب :

1. `pip install django-guardian`

نکته : اگر در نصب پکیج ها با بخاطر اینترنت با مشکل مواجه شدیم، میتوانیم از میرور های داخلی هم استفاده کنیم :
`https://docs.runflare.com/mirror/pypi-mirror/`

2. in INSTALLED_APPS : `'guardian'`

3. در ستینگز این موارد را باید اضافه کنیم :

```
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)
```

3. `python mange.py migrate`

4. دوتا جدول برای پروژه ما ایجاد میکند:

`guardian_groupobjectpermission`
`guardian_userobjectpermission`

5. در ستینگز این تنظیمات را انجام میدهیم :

```
GUARDIAN_MONKEY_PATCH_GROUP = True
GUARDIAN_MONKEY_PATCH_USER = True
```

6. برای افزودن سیستم مدیریت این پکیج برای پنل ادمین، می بایست در هر اپی که لازم داشتیم در فایل ادمین آن مدل، تنظیمات آن
   را اضافه کنیم، مثلا در ادمین ماژول محصولات، بجای ارث بری از مدل ادمین خود جنگو، از گارددمدل ادمین ارث بری میکنیم:

```
from django.contrib import admin
from . import models
from guardian.admin import GuardedModelAdmin


class ProductAdmin(GuardedModelAdmin):
    list_filter = ['category', 'is_active']
    list_display = ['title', 'price', 'is_active', 'is_delete']
    list_editable = ['price', 'is_active']
```

7. الان، اگر بریم داخل یکی از محصولات در پنل ادمین، گزینه زیر را مشاهده میکنیم:

`OBJECT PERMISSIONS`

8. در این صفحه، ما میتوانیم برای لیست کاربران، و یا لیست مربوط به گروه ها، پرمیشن هایی که میخوایم رو اضافه کنیم؛ یعنی
   ابتدا آیدی یوزر را میدیم تا او را پیدا کند، سپس منیج یوزر را زده و اینجا برای آن محصول انتخابی، میتوانیم پرمیشن هایی
   را ست کنیم و ذخیره میکنیم. این اطلاعات در جدول گاردین یوزرآبجکت پرمیشن ذخیره میشود.

9. برای مدل های دیگر خودمان هم به همین روش انجام میدهیم، مثلا برای دسته بندی محصولات:

```
@admin.register(models.ProductCategory)
class ProductCategoryAdmin(GuardedModelAdmin):
    pass
```