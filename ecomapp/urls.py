from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = "ecomapp"
urlpatterns = [
    path("" , HomeView.as_view(), name='home'),
    path("about/" , AboutView.as_view(), name='about'),
    path("contact/" , ContactView.as_view(), name='contact'),
    path("all-products/", AllProductsView.as_view(), name="allproducts"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="productdetail"),
    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("register/", CustomerRegistrationView.as_view(), name="customerregistration"),
    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),
    path("login/", CustomerLoginView.as_view(), name="customerlogin"),
    path("dashboard2/", DashboardView.as_view(), name="dashboard2"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),

    path("checkout/",CheckoutView.as_view(), name="checkout"),
    path("payment/", PaymentView.as_view(), name = "payment"),
    path('changeaddress/', ChangeAddressView.as_view(), name ='changeaddress'),
    #path("forgetpassword/", CustomerForgetPasswordView.as_view(), name="customerforgetpassword"),
    path("passwordchange/", PasswordChangeView.as_view(), name="passwordchange"),
    #path("", PasswordChangeDoneView.as_view(), name="passwordchangedone"),
    path('search/', SearchView.as_view(), name="search"),
    path('success/', success, name="success,"),
    

    




]