# Article Module

## parent_id

ما میتوانیم کاری کنیم که یک مدل با خودش رابطه داشته باشد، یعنی ما یک مدل داریم به اسم آرتیکل کتگوری که دسته بندی مقاله
هست، از طرفی هر دسته بندی میتواند زیر مجموعه هایی هم داشته باشد، مثلا دسته بندی والد یا اصلی داریم به اسم کالای دیجیتال،
که مواردی مثل موبایل، لپ تاپ و غیره میتوانند شاملش شوند؛ یا دسته بندی والدی داریم به اسم پوشاک، که فرزندان یا زیردسته
بندی هایش میتوانند شامل پیراهن، شلوار، جوراب و غیره باشند؛ از این رو بعد از ساخت کلاس مدل و ایجاد رابطه در آن و زدن
مایگریشن، در جدول ایجاد شده یک پرنت آیدی هم اضافه میشود که اگر مقدارش نال باشد، یعنی آن دسته بندی، دسته بندی اصلی است،
ولی اگر آیتمی وجود داشته باشد که زیردسته بندی باشد، مقدار پرنت آیدی میشود همان مقدار دسته بندی والد؛ کلاس مدل دسته بندی
مقالات که رابطه با خودش دارد، به شکل زیر است:

```
class ArticleCategory(models.Model):
    parent = models.ForeignKey('ArticleCategory', null=True, blank=True, on_delete=models.CASCADE, verbose_name='دسته بندی والد')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    url_title = models.CharField(max_length=200, unique=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقاله'
```

در این ساختاری که پیاده سازی کرده ایم، ما میتونیم تا بی نهایت لول داخل برویم، به این منظور که مثلا کالای دیجیتال میتواند
زیر شاخه موبایل را شامل شود، دوباره همین موبایل میتواند یک زیر شاخه ی دیگر به اسم سامسونگ داشته باشد، در زیر شاخه لول
بعد میشود سری اس، سری ای و ... همین جور الی آخر، پس میتونیم چرخه ی بی نهاتی در دسته بندی هامون پیاده سازی کنیم.

## ManyToMany

رابطه ی بین دسته بندی مقالات و خود مقالات رو چند به چند درنظر میگیریم، چون که هر مقاله میتواند در دسته بندی های مختلفی
قرار بگیرد و از آن طرف هم هر دسته بندی میتواند چندین مقاله را در خود داشته باشد:

```
class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=400, db_index=True, allow_unicode=True, verbose_name='عنوان در url')
    image = models.ImageField(upload_to='images/articles', verbose_name='تصویر مقاله')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    text = models.TextField(verbose_name='متن مقاله')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    selected_categories = models.ManyToManyField(ArticleCategory, verbose_name='دسته بندی ها')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
```