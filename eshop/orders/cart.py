from home.models import Product

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)  # اطلاعات سبد خرید کاربر داخل سشن کارت ذخیره میشن
        if not cart:  # اگر نان بود یعنی کاربر بار اوله که سبد خرید داره و برای اون یه سبد خرید اضافه میکنه
            cart = self.session[CART_SESSION_ID] = {}  # ایجاد سبد خرید
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()  # کل کلیدها را میگیریم
        products = Product.objects.filter(
            id__in=product_ids)  # داخل محصولات بگرد انهایی که ای دیشون یکی ازproduct_ids بود بیاور بیرون
        cart = self.cart.copy()  # چون قراره سبد خرید تغیر کنه پس  یه کپی میگیریم که سبد خرید اصلی عوض نشه
        for product in products:
            cart[str(product.id)]['product'] = product  # اسم محصول را به سشن اضافه کردیم

        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']  # قیمت کل را حساب کردیم چندتا محصول قیمتشون چند است
            yield item  # اطلاعاتyield  را تکه تکه برمیگرداند برخلاف returnکه همه را باهم برمیگرداند

    def __len__(self):#شمارش تعداد محصولات
        return sum(item['quantity'] for item in self.cart.values())



    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:  # 'اگه محصول داخل سبد خرید نبود
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}  # یکی براش ایجاد کن
        self.cart[product_id]['quantity'] += quantity  # اگه داخل سبد خرید بود به تعداد اضافه کن
        self.save()

    def remove(self, product):#حذف محصولات
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):#حمع کل قیمت محصولات  در پایین لیست
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())



    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()