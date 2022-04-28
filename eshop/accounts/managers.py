from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,phone_number, email,full_name, password):#چیزایی که قراره به کاربر نشون بدهیم و کاربر کامل کنه
        #برای اعتبار سنجی است و فقط پسورد را خود جنگو اعتبار سنجی میکنه
        if not phone_number:
            raise ValueError('کاربر باید حتما دارای شماره تماس باشد')
        if not email:
            raise ValueError('کاربر باید حتما دارای ایمیل باشد')

        if not full_name:
            raise ValueError('کاربر باید حتما دارای نام و نام خانوادگی  باشد')

        user = self.model(phone_number=phone_number, email=self.normalize_email(email), full_name=full_name)

        user.set_password(password)#همیشه پسورد را با ست پسور ذخیره میکنیم تا پسوردها هش یشن و مستقیم مثل شماره تماس و اینا ذخیره نمیکنیم
        user.save(using=self._db)#تا دیتابیسی که فعاله فراخوانی بشه
        return user


    def create_superuser(self,phone_number, email,full_name, password):
        user = self.create_user(phone_number, email,full_name, password)#اینcreate_user را تا پسورد ست  فراخوانی کن و استفاده کن فقط is_adminرا True بزار
        user.is_admin = True
        user.save(using=self._db)
        return user

