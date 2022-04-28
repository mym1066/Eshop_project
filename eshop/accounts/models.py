from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import UserManager

# Create your models here.

#AbstractBaseUserبه طور پیش فرض بعضی فیلدهای مدل را داخل خودش داره وو ما فقط بعضی را اضافه میکنیم
#AbstractUser همه فیلدها را داره و لازم نیست ما اضافه میکنیم و بهتر از بالایی استفاده کنیم



class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)#unique ایمیل منحصربفردباشه پس از این استفاده میکنیم
    phone_number = models.CharField(max_length=11, unique=True)#unique  منحصربفردباشه پس از این استفاده میکنیم
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)#هر کاربر در حالت اولیه فعال یاشه پس دیفالت فعال باشه
    is_admin = models.BooleanField(default=False) #کاربر در حالت اول ادمینه هست یا نه اول میزرایم نه بعد اگه بود دستی تورو میکنیم

    objects = UserManager()#ارتباط با فایل منیجر تا یوزر از منیجر استفاده کنه


    USERNAME_FIELD  ='phone_number'  #فیلدی که کاربر باهاش اعتبار سنجی میشه نباید تکراری باشه و باید حتما خاص و منحصربفرد باشه
    REQUIRED_FIELDS = ['email', 'full_name']# وقتی سوپر یوزر را میزنیم چه فیلدهایی را درخواست کنیم فیلدهای اجباری را داخل لیست میزاریم

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):#یک نمونه جدید را استفاده کردیم ب هصورت شی نشون نده به صورت رشته نشون بده __str__ یعنی نشان دادن برنامه به کاربر
        return self.email

    #def has_perm(self, perm, obj=None):  # ایا کاربر دسترسی خاضی داره
    #    return True  #کاربر هر دسترسی  که میخاد بهش میدیم برای همین تورو میزاریم

   # def has_module_perms(self, app_label):#ایا کاربر به مدل ها دسترسی دارد یا ن
        #app_lableبه مدل های کدوم اپ دسترسی داشته باشه
   #     return True
# چون در حالت بالا باز هم کاربر به همه چی دسترسی دارد پس چون از پرمیشن میکسینگ  استفاده میکنیم دیگه نیازی به دوتای بالایی نیست چون پرمیشن میکسینگ در  خودش دارد این دو را





    #کابرانی که اجازه ورود به کنترل چپنل را دارند
    @property#   رفتارش بشه مثل  is_adminو is_active
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):#کدی که ما ارسال کردیم
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'

    class Meta:
        verbose_name = 'کد ارسالی '
        verbose_name_plural = 'کدهای ارسالی'


