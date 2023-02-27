from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View, TemplateView, CreateView, FormView
from main.models import *
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myname'] = 'yashanki'
        context['product_list'] = Product.objects.all().order_by("-id")

        return context


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(TemplateView):
    template_name = "contact.html"


class DashboardView(TemplateView):
    template_name = "dashboard2.html"


class ProductDetailView(TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count = +1
        product.save()
        context['product'] = product
        return context


class AllProductsView(TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


'''def add_to_cart(request, slug):
    product = Product.objects.get(slug=slug)
    user = request.user
    product.save()
    user.save()'''




class AddToCartView(TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return context
   


        

class MyCartView(TemplateView):
    template_name = "mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context
    def get(self,request, **kwargs):
        
        client = razorpay.Client(
        auth=(settings.KEY, settings.SECRET))
        order_amount = (500)*100
        order_currency = "INR"
        
        payment = client.order.create(
                {'amount': order_amount, 'currency': order_currency, 'payment_capture': 1})
        payment = payment['id']
        
        context ={
            "amount" : order_amount,
            "payment" : payment,
        
    

        }
        return render(request, "payment.html", context) 
@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key ,val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
            print(order_id)

        #user = Order.objects.filter(payment=order_id).first()
        #user.paid = True
        #user.save()
    return render(request, "thankyou.html")






class ManageCartView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("ecomapp:mycart")


class EmptyCartView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("ecomapp:mycart")


class CheckoutView(CreateView):
    template_name = "payment.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("ecomapp:payment")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
            pm = form.cleaned_data.get("payment_method")
            order = form.save()
            if pm == "razorpay":
                return redirect(reverse("ecomapp:payment") + str(order.id))

            else:
                return redirect("ecomapp:home")
        else:
            return super().form_valid(form)
        
        


class ChangeAddressView(TemplateView):
    template_name = 'changeaddress.html'
    form_class = ChangeAddressForm
    success_url = reverse_lazy("ecomapp:payment")

    '''def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        shipping_address = request.GET.get("shipping_address")
        change_address = request.POST("change_address")
        user = authenticate(shipping_address=shipping_address,
                            change_address=change_address)
        if shipping_address != change_address:
            cart_shipping_address = Cart.objects.get.filter(
                id = shipping_address).update(id=change_address)
            cart_shipping_address.save()
        else:
            return

        return context'''


class PaymentView(View):
    template_name = "payment.html"



class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomapp:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        user.save()
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomapp:home")


class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy('ecomapp:home')

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)

        if usr is not None and usr.customer:
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid Credentials"})
        return super().form_valid(form)


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Product.objects.filter(Q(title__icontains=kw))
        print(results)
        context["results"] = results
        return context


class PasswordChangeDoneView(FormView):
    template_name = "passwordchangedone.html"
    form_class = PasswordChangeForm
    login_url = reverse_lazy('ecomapp:login')
    success_url = reverse_lazy('ecomapp:home')


class PasswordChangeView(FormView):
    template_name = "passwordchange.html"
    form_class = PasswordChangeForm
    login_url = reverse_lazy('ecomapp:login')
    success_url = reverse_lazy('ecomapp:home')

    def form_pass_update(self, form):
        uname = form.cleaned_data.get("username")
        newpass = form.cleaned_data.get['newpassword']
        user = authenticate(username=uname, newpassword=newpass)
        form.instance.user = user

        return super().form_valid(form)

    '''def get_form_kwargs(self):
        context = super().get_form_kwargs()
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data.get("newpassword"))
        user.save()
        messages.success={self.request, "password changed successfully"}
        return super().form_valid(form)   '''

    '''oldpass =form.cleaned_data["oldpassword"]
        newpass =form.cleaned_data["newpassword"]
        #user =User.authenticate(username, oldpassword, newpassword)
        form.instance.user = user
        
        user = authenticate(username=uname, oldpassword=oldpass, newpassword=newpass)
        if oldpass != newpass in user.customer:
            user.save()
        else:
           return render(self.request, self.template_name, {"form": self.form_class, "error": "oldpassword and password2 are not same"})'''

    def get_cart_total(self, request):
        cp_id = self.kwargs["cp_id"]
        # action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        cp_obj.subtotal


# Create your views here.
