from django.db import models
from django.contrib.auth import get_user_model
from home.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.




class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders') #سفارش مربوط به کدوم کابر است
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    discount = models.IntegerField(blank=True, null=True, default=None)#درصئدر که قراره تخفیف بخوره

    class Meta:
        ordering = ('paid', '-updated')
        verbose_name = 'سفارش '
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return f'{self.user} - {str(self.id)}'

    def get_total_price(self):
        total = sum(item.get_cost()for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total#اگر کد تخفیف وجود داشت از مبلغ کل کم میکنیم
            return int(total - discount_price)
        return total

class OrderItem(models.Model):#محصولاتی که داخل سفارش بوده را مشخص میکند
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='order_items')
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity



class Coupon(models.Model):#مشخص کردن کد نخفیف و داخل مدل ها ذخیره میکنیم
       code = models.CharField(max_length=30, unique=True)# unique=Trueتا کد تخفیف تکراری صادر نشه
       valid_from = models.DateTimeField()#کد تخفیف از چه زمانی شروع میشه
       valid_to = models.DateTimeField()#کد تخفیف تا کی اعتبار داره
       # مشخص کردن اعدادی بین 0 تا90برای discount
       discount =models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(90)]) #چه مقدار تخفیف داده شود
       active = models.BooleanField(default=False)#کد تخفیف فعال هست یا خیر

       def __str__(self):
           return self.code

       class Meta:
           verbose_name = 'تخفیف '
           verbose_name_plural = 'تخفیفات'




