from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm
import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone'], random_code)  # ارسال اس ام اس
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)  # ارسال کد تایید
#استفاده میکنیم و اطلاعات داخل مرورگر خود کاربر ذخیره مکیشه و میتوان بعد اطلاعات را از مرورگر کاربر گرفته و ان را بشناسیم و مستونه اطلاعات خودش را تغیر بده session برای ذخیره اطلاعات کاربران از
            # اطلاعات کابر را گرفته و داخل سشن ذخیره میکنیم و کاربر را به یک ویو دیگه ارسال میکنیم . اگر کاربر کد را درست وارد کنه اطلاعات داخل سشن را گرفته و ثبت نام میکنیم ولی اگه کاربر کد را درست تحویل نده اطلاعات کاربر مهم نیست و ثبت نام نمیشه
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'ما یک کد برای شما ارسال کردیم', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['phone_number'], user_session['email'],
                                         user_session['full_name'], user_session['password'])
                code_instance.delete()  # وقتی کاربر ثبت نام کرد دیگه احتیاجی به کد نیست پس از دیتابیس حذف کن
                messages.success(request, 'شما با موفقیت ثبت نام کردید', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'کد وارد شده متعبر نمیباشد', 'danger')
                return redirect('accounts:veryfi_code')
        return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):#فرم را میگیزریم و به کاربر نشون میدیم
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):#کاربر اطلاعات را وارد کرد
        form = self.form_class(request.POST)#میگیریم و میریزم داخل داخل فرم
        if form.is_valid():#بررسی اطلاعات
            cd = form.cleaned_data#اگه درست بود میریزیم داخل  سی دی
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])#شماره تلفن و پسورد به هم میخوره یا نه
            if user is not None:
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد شدید', 'info')
                return redirect('home:home')
            messages.error(request, 'تلفن یا ایمیل شما اشتباه است', 'warning')
        return render(request, self.template_name, {'form': form})

#LoginRequiredMixin لاگین کردن کاربر را بررسی میکند
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'شما با موفقیت خارج شدید', 'success')
        return redirect('home:home')
