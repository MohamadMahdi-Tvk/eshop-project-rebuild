# Customize Admin Panel

ادمین جنگو، با اینکه به شدت پرکاربرد هست و خیلی امکانات زیادی برای ما فراهم میکند، در بیشتر موارد هم اذیت کننده میشود؛
البته پکیج هایی هستند که نصب کنیم و ظاهری که دوست داریم را برایش درنظر بگیریم، که برخی از آنها پولی هستند و بعضی از آنها
رایگان هستند؛ اما در کل باز هم میشه کاری کرد که مدیریت آن دقیقا جوری باشد که ما میخواهیم؛ در اینجا میتوانیم از قالب های
آماده پنل ادمین استفاده کنیم. اگر خواسته باشیم بجای پنل ادمین خود جنگو از قالب دیگری استفاده کنیم، دردسر زیادی خواهد
داشت و کارهای زیادی باید انجام بدیم تا بتوانیم قالب دیگری را با قالب خود ادمین جنگو جایگزین کنیم. اما میتوان یک کار
دیگری انجام داد، دست به ادمین جنگو نمیزنیم، اما میایم یک اپ جدید میسازیم و یک لایوت جدید برایش درنظر میگیریم و قالب را
منتقل میکنیم و طوری پیاده سازی میکنیم که انگار داریم پروژه جدید ولی با قالب ادمین پیاده سازی میکنیم.

1. `python manage.py startapp admin_panel`

2. ما برای این پنل اختصاصی خودمان باید همه چیز را بنویسیم و مثل پنل خود جنگو همه چیز پیاده سازی نمیشود؛ بنابراین طبق آن
   چیزی که نیاز داریم پنل ادمین اختصاصی ما داشته باشد، آن را پیاده سازی میکنیم.

## reverse_lazy :

در کلاس بیس ویو ها بجای استفاده از ریورس برای یوآرال ها باید از دستور ریورس لیزی استفاده کنیم، خود ریورس برای اینکه کلاس
بیس ویو ها در پس زمینه یکسری عملیاتی رو انجام میدهد، درست کار نمیکند و قصد دارد همان لحظه برای ما آن آدرسی که بهش میدیم
رو بدست بیاورد، اما این قابلیت رو ریورس ندارد؛ بجای آن از ریورس لیزی استفاده میکنیم، یعنی میگه برو هر فعالیتی که داری
انجام بده و هروقت که تونستی آن آدرس رو هم بردار بیار:

```
class ArticleEditView(UpdateView):
    model = Article
    template_name = 'admin_panel/articles/edit_article.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_articles')
```

## django-widget-tweaks:

این پکیج این امکان رو میده که زمانی که داریم با فرم ها کار میکنیم، اون فیلد هایی که هر فرم دارد رو اونجور که میخواهیم
ویرایش کنیم.

1. `pip install django-widget-tweaks`

2. in settings.py : `'widget_tweaks'`

3. در هر تمپلیت ویویی که خواستیم میتوانیم آن را لود کنیم:

`{% load widget_tweaks %}`

4. طبق ساختار زیر میتونیم از آن استفاده کنیم :

```
{% extends 'admin_panel/shared/_admin_layout.html' %}
{% load widget_tweaks %}

{% block title %}ویرایش مقاله{% endblock %}

{% block content %}
    <div class="row">
        <div class="col-md-12">
            <div class="widget">
                <div class="widget-header bordered-top bordered-warning">
                    <span class="widget-caption">ویرایش اطلاعات مقاله با عنوان {{ article.title }}</span>
                </div>
                <div class="widget-body">
                    <div class="collapse in">
                        <form action="{% url 'admin_edit_article' pk=article.id %}" method="post" enctype="multipart/form-data">
                            {% csrf_token %}
                            {% for field in form %}
                                <div class="form-group">
                                    <label for="id_{{ field.name }}">{{ field.label }}</label>
                                    {% render_field field class='form-control is-invalid' %}
                                    <div>
                                        <ul>
                                            {% for error in field.errors %}
                                                <li class="text-danger">{{ error }}</li>
                                            {% endfor %}
                                        </ul>
                                    </div>
                                </div>
                            {% endfor %}
                            <div class="row">
                                <div class="col-md-3">
                                    <button type="submit" class="btn btn-warning btn-block">ویرایش</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
{% endblock %}
```