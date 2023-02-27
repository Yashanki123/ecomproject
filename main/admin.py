from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register([Customer ,Product, Category, CartProduct, Cart, Order])


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ('username','email','address','password','user')
admin.site.register(Customer,CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('title', 'category','image','marked_price','selling_price','description','warranty','return_policy')
admin.site.register(Product, ProductAdmin )    

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('title','slug')
admin.site.register(Category, CategoryAdmin)

class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('id','customer', 'total','created_at',"razorpay_order_id", "razorpay_payment_id","razorpay_payment_signature")
admin.site.register(Cart,CartAdmin)


class CartProductAdmin(admin.ModelAdmin):
    model = CartProduct
    list_display = ('id', 'cart', 'product', 'rate', 'quantity', 'subtotal')
admin.site.register(CartProduct, CartProductAdmin)    


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display=('ordered_by',"order_id","shipping_address",'email','subtotal','total','order_status','created_at','payment_method','paid','payment_completed')
admin.site.register(Order, OrderAdmin)


