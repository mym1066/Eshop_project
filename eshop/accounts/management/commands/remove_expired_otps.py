from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta
import pytz


class Command(BaseCommand):
    help = 'remove all expired otp codes'

    def handle(self, *args, **options):
        expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)#تاریخ الن منهای دو دقیقه قبل
        OtpCode.objects.filter(created__lt=expired_time).delete()#اونهایی که از دو دقیقه قبل بودن را بیاورو حذف کن
        self.stdout.write('all expired otp codes removed.')


