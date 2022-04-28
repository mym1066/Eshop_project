from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChengeForm
from .models import User, OtpCode
from django.contrib.auth.models import Group

# Register your models here.

#ثبت نام با شماره تلفن
@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number','code', 'created')





class UserAdmin(BaseUserAdmin):
    form = UserChengeForm
    add_form = UserCreationForm#چوا ما میخواهیم از یک فرم دیگه هم استفاده کنیم بنابراین ازadd_form استفاده میکنیم

    list_display = ('email', 'phone_number', 'is_admin')#نحوه نمایش که کدوم فیلد نمایش داده بشه
    list_filter =('is_admin',)# کاربرها بر اساس چی فیلتر بشن
    # برای form
    readonly_fields =('last_login',)

    fieldsets = (
        #هر چی به جای None بزااریم به عنوان عنوان این قسمت نمایش میده
        (None, {'fields': ('email', 'phone_number', 'full_name', 'password')}),
        ('Permissions', {'fields':('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),

    )#مجموعه از اینپوت ها را نمایش بده

#برای add_form
    add_fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'full_name', 'password1', 'password2')}),

    )

    search_fields = ('email', 'full_name')#برای سرچ کاربرها از کدوم فیلد استفاده کنه
    ordering = ('full_name',) #کاربرها بر اساس چی مرتب کنه
    filter_horizontal = ('groups', 'user_permissions')#قراردادن دو مقدار کنار هم

    def get_form(self, request, obj=None, **kwargs):
        #کاربری که از اول یوزرامین نبوده براش غیر فعال میشهکه نتونه فعالش کنه
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form




#admin.site.unregister(Group)حذف میکنیم تا گروه برای کاربران بیاید
admin.site.register(User,UserAdmin)
