from django.db import models
from django.urls import reverse#کامل یوارال ها را دربیاره
from ckeditor.fields import RichTextField


# Create your models here.
class Category(models.Model):
    # باید  null , blankبزاریم true  چون ممکن است زیردسته خالی باشه و ذسته بندی کلی داشته باشیم
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)#کلید خارجی باید وارد بشه به خود این کتگوری و با سلف اینکار را میکنیم و رابطه را ایجاد میکنبم
    is_sub = models.BooleanField(default=False)#دسته بندی کلیه یا زیرمجموعه
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)  #  با slug میگیک از چه کتگگوری استفاده میکنیم و با unique میگیم slug تکراری نداشته باشیم

# از کلاس متا استفاده میکنیم یعنی یه کار اضافه انجام بدیم
    class Meta: #تغیر رفتار سایر کلاس ها
        ordering = ('name',)
        verbose_name = 'دسته بندی '
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug,])#ارگومانها را براساس اسلاگ می اوریم




class Product(models.Model):
    #  برای اینکه بدونیم هر محصول به کدام دسته تعلق داره از این ForeignKey استفاده میکنیم ولی وقتی زیردسته ها رامشخص کردیم باید رابطع چندبه چند بشه و دیگه به on_delete=models.CASCADE,  نیازی نداریم
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField()
    description = RichTextField()
    price = models.IntegerField()#این decimal_placesتعداد اعشار را میگه و این  max_digits  رقم عدد
    available = models.BooleanField(default=True)#محصول موجود هست یا خیر
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.name

    def get_absolute_url(self):#راحتر  ریدایرکت کردن کابر به صفحه جزییات
        return reverse('home:product_detail', args=[self.slug,])#ارگومانها را براساس اسلاگ می اوریم
