# prefetch_related

این مورد در نظرات و پاسخ نظرات کاربران برای بخش مقالات پیاده سازی شده است؛ ما اگر از این دستور استفاده نکنیم، مشکلی که
بوجود میاد این هست که اگر بطور مثال مقاله 100 کامنت داشته باشد و هرکدام از آنها یک پاسخ داشته باشند، اتفاقی که میفتد این
هست که بجای اینکه بیاد و در یک کوئری به دیتابیس، همه ی دیتا را واکشی کند، عملا 101 کوئری به دیتابیس زده میشود، یعنی یک
کوئری در ویوی خود زدیم برای واکشی کامنت های اصلی و همینطور در خود تمپلیت هم به ازای هر 100 کامنتی که وجود دارد، یک کوئری
دیگر میزند که پاسخ هایش را واکشی کند؛ برای جلوگیری از این اتفاق باید بتوانیم همه ی دیتا رو در یک کوئری واکشی کنیم،
بنابراین از دستور پریفچ ریلیتد استفاده میکنیم و با این دستور میگیم برو پاسخ هایش را هم جوین بزن و بیار، یعنی اگر 100 تا
نظر میاری، پاسخ هاشون هم در یک کوئری بیار؛ این بحث پرفرمنسی است:

```
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail_page.html'

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        article: Article = kwargs.get('object')
        context['comments'] = ArticleComment.objects.filter(article_id=article.id, parent=None).prefetch_related('articlecomment_set')
        return context
```