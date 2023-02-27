from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    password = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)

    #joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



class Category(models.Model):
    title = models.CharField(max_length=225)
    slug = models.SlugField(unique=True)

    def save(self, *args,**kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args , **kwargs)



    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=225)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()
    warranty = models.CharField(max_length=300, null=True, blank=True)
    return_policy = models.CharField(max_length=225)
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args ,**kwargs)


    def __str__(self):
        return self.title

class Cart(models.Model):
    customer = models.OneToOneField(Customer , on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at =models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_signature = models.CharField(max_length=100, null=True, blank=True)



    def __str__(self):
        return "Customer" + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    
    quantity = models.PositiveIntegerField()
    total = models.PositiveIntegerField(null=True)
    subtotal = models.PositiveBigIntegerField()

    def __str__(self):
        return "Cart:" + str(self.cart.id) + "CartProduct:" + str(self.id)


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Cancelled", "Order Cancelled"),
    

)

METHOD=(
    ("Cash On delivery", "Cash On delivery"),
    ("razorpay", "razorpay")
)

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE )
    order_id = models.CharField(max_length=100, blank=True)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField(null=True, blank=True)
    total = models.PositiveIntegerField(null=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at =models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=METHOD, default=True)
    paid = models.BooleanField(default=False)
    payment_completed = models.BooleanField(default=False, null=True, blank=True)

def __str__(self):
    return self.order.user.username  





