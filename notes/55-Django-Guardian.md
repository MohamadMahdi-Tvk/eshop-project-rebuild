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

## Permission Checker in Guardian

ما برای سطح دسترسی ها چند تا مورد را باید چک کنیم؛ قدم اول اینکه آیا کاربر به صفحه مثلا پنل مدیریت اختصاصی که ایجاد کرده
ایم دسترسی دارد و میتواند آن را مشاهده کند، و قدم دوم، در لیست مثلا مقالات، کدام آیتم ها را میتواند مشاهده کند. تفاوت
های دو جدول زیر :

`account_module_user_user_permissions` :
این جدول برای ذخیره سازی پرمیشن های گلوبال هست، یعنی مشخص میکند یک یوزری، چه دسترسی رو دارد.

`guardian_userobjectpermission` :
اگر بخواهیم برای هر آبجکت به کاربر پرمیشن بدهیم، در این جدول ذخیره میشود.

بطور مثال در نمایش لیست مقالات در پنل ادمین اختصاصی، دو مورد را چک کردیم، با استفاده از دستور زیر:

`permission_required = ['article_module.view_article']`

صرفا چک میکند که ما به صفحه لیست مقالات دسترسی داریم یا خیر و با آبجکت های آن کاری ندارد.

و در قسمت زیر :

```
query = get_objects_for_user(
   user=self.request.user,
   perms=self.permission_required,
   klass=query,
   accept_global_perms=False,
)
```

گفتیم فقط آبجکت هایی را بیار که واقعا دسترسی داریم، یعنی برای دسترسی به المان های داخل صفحه

یک فانکشن گت_آبجکت_فورگروپ هم داریم که برای گروها میتوان از آن استفاده کرد.

## assign_perm

با این دستور میتوان یک پرمیشن برای یوزر و آن آبجکت خاص ثبت کرد، یعنی ما با این دستور، دسترسی آبجکتی رو به کاربری میدهیم؛
این دستورات را میتوان در شل جنگو انجام داد:

`assign_perm("view_article", user, article)`

یا با دستور زیر، برای تمامی مقالات دسترسی ثبت میشود، یعنی ما میتوانیم کوئری ست هم پاس بدیم:

`assign_perm("view_article", user, Article.objects.all())`

## guardian_tags

در صفحات تمپلیت ویوی خود باید آن را لود کرده و میتوان مدیریت کرد که مثلا اگر دسترسی وجود نداشت، دکمه ی ویرایش را نمایش
ندهد:

```
{% load guardian_tags %}

{% for article in object_list %}
   {% get_obj_perms user for article as 'article_perms' %}
   <tr>
       <td>{{ article.title }}</td>
       <td>
           {% if article.is_active %}
               <span class="text-success">فعال</span>
           {% else %}
               <span class="text-danger">غیرفعال</span>
           {% endif %}
       </td>
       <td>
           {% if "change_article" in article_perms %}
               <a href="{% url 'admin_edit_article' pk=article.id %}" class="btn btn-warning">ویرایش
                   محصول</a>
           {% endif %}
       </td>
   </tr>
{% endfor %}
```

## Creating separate permission tables for each model class

در زمانی که میزان اطلاعات ما زیاد شود، ممکن هست در مبحث پرفرمنس به مشکل برخورد کنیم، به این دلیل که تمامی دسترسی های
جدول در دو جدول، که یکی برای یوزر هست و یکی برای گروه، ذخیره میگردند، اما ما میتوانیم به ازای هر مدلی که میخواهیم این دو
جدول رو ایجاد کنیم، بطور مثال برای مدل مقاله ما میتوانیم به این صورت دو مدل دیگر برای یوزر و برای گروه به آن متصل کنیم:

```
class ArticleUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="article_user_object_permission",
    )

    class Meta(UserObjectPermissionBase.Meta):
        db_table = 'article_user_object_permission'


class ArticleGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="article_group_object_permissions",
    )

    class Meta(GroupObjectPermissionBase.Meta):
        db_table = 'article_group_object_permissions'
```

و سپس مایگریشن میزنیم تا جداول ساخته شوند. و از این به بعد پرمیشن ها به جداول جداگانه ای که ما ایجاد کرده ایم اضافه و
ذخیره میشوند و دیگر در جدول خود گاردین ذخیره نمیشوند. و در این حالت در پردازش و واکشی اطلاعات سرعت بیشتر شود. پس برای
مواردی که میدانیم تعداد آیتم ها ممکن هست زیاد شوند از همین روش استفاده میکنیم، ولی برای مواردی که تعداد آیتم ها کم هستند
مثل دسته بندی ها و غیره، از همان روش پیش فرض خود گاردین استفاده میکنیم.

## Sample code for working with Guardian in the Django shell

1. `python manage.py shell`
2. `from guardian.shortcuts import assign_perm, remove_perm`
3. `from article_module.models import Article`
4. `from account_module.models import User`
5. `user = User.objects.get(username="admin2")`
6. `article = Article.objects.first()`
7. `assign_perm("view_article", user, article)`
8. `assign_perm("change_article", user, article)`
9. `remove_perm("change_article", user, article)`

## Fix Login

چون ما مورد زیر را برای احراز هویت پکیج گاردین اضافه کردیم:

```
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)
```

در لاگین کردن یوزر به مشکل میخوریم، چون ما یک بک اند جدید اضافه کرده ایم؛ و مدل بک اند ما بصورت پیش فرض روی مدل بک اند
خود جنگو تنظیم شده بود، و ما اومدیم یک بک اند جدید اضافه کرده ایم؛ ما در فانکشن لاگینی که پیاده سازی کرده ایم، میتوانیم
بک اند را تنظیم کنیم تا دیگر ارور ندهد:

```
if is_password_correct:
    user.backend = "django.contrib.auth.backends.ModelBackend"
    login(request, user)
    return redirect(reverse('user_panel_dashboard'))
```

## Guardian Document

پیشنهاد میشود برای یادگیری بیشتر این پکیج، داکیومنت رسمی آن مطالعه شود:

`https://django-guardian.readthedocs.io/en/stable/`

