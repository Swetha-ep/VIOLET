from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from app.models import Product
# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now=True)

    def __str__(self):
        return self.cart_id
    



class Cartt(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)


   

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default = True)

    def sub_total(self):
        return self.product.selling_price * self.quantity

    def __str__(self):
        return self.product
    


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    orderstatuses = (
        ('Pending' , 'Pending'),
        ('Out For Shipping' , 'Out For Shipping'),
        ('Completed','Completed'),

    )
    status = models.CharField(max_length=150,choices=orderstatuses,default='Pending')
    message = models.TextField(null = True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)
    
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50)
    discount = models.BigIntegerField()
    minimum_purchase = models.BigIntegerField()
    is_active = models.BooleanField(default=False)

    def str(self):
        return self.coupon_code
    
class CouponUsed(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE, blank=True, null=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE, blank=True, null=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)    
    price = models.FloatField(null = False)
    quantity = models.IntegerField(null=False)


    def __str__(self):
        return '{} {}'.format(self.order.id, self.order.tracking_no)
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    phone = models.BigIntegerField(null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.BigIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    



