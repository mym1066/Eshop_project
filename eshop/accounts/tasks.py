from celery import shared_task
from accounts.models import OtpCode
from datetime import datetime,timedelta
import pytz

@shared_task
def remove_expired_otp_codes():
    expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)  # تاریخ الن منهای دو دقیقه قبل
    OtpCode.objects.filter(created__lt=expired_time).delete()  # اونهایی که از دو دقیقه قبل بودن را بیاورو حذف ک