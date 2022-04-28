from django import forms
from .models import User, OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)  # برای تغییر  فرم ها استفاده میشن

    class Meta:  # کلاسی که اجازه میده رفتار بقیه کلاس ها را تغیر دهید
        model = User
        fields = ('email', 'phone_number', 'full_name')

    # برابر بودن پسورد 1 و 2
    def clean_password2(
            self):  # دوتا پورد شبیه هم باشند پسورد 2 را انتخاب میکنیم تاقبل ان پسورد 1 ایجاد شده باشه وارور نده
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('پسورد یکسان نیست ')
        return cd['password2']

    # هش کردن پسورد
    def save(self, commit=True):
        # فعات ذخیره نشو تا یه چیر دیگه ارسال کنم نمیخواهیم مدل  را ذخیره کنیم - ما می‌خواهیم ابتدا پس.رد را هش  کنیمcommit=False
        user = super().save(commit=False)  # به اعضای کلاس مادر دسترسی داشته باشیمsuper
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# تغیر اطلاعات کاربر
class UserChengeForm(forms.ModelForm):
    # پسورد را به صورت هش شده فقط نشون میده و قابل تغییر نیست ReadOnlyPasswordHashField
    password = ReadOnlyPasswordHashField(help_text="برای تغییر رمز <a href=\" ../password/\"> اینجا </a> کلیک کنید")

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')


class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField(label=' full name')
    phone = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)

    # کاربر شماره تلفن و ایمیل تکراری وارد نکنه
    def clean_email(self):
        email = self.cleaned_data['email']  # کاربر ایمیل تکراری وتارد نکنه
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('ایمیل قبلا وارد شده')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']  # کاربر شماره تکراری وتارد نکنه
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('این شماره قبلا وارد شده')
        OtpCode.objects.filter(phone_number=phone).delete()
        return phone


class VerifyCodeForm(forms.Form):  # کاربر عدد رندمی که براش ارسال کردیم را برای ما ارشال کنه
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
