from django import forms
from main.models import *
from django.contrib.auth.models import User

class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    

    class Meta:
        model = Customer
        fields = ["username", "password", "email", "address"]

    #def clean_username(self):
        #uname = self.cleaned_data.get("username")
        #user=Customer.objects.filter(username=uname)
        #return user 
        
            
        


class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())      

          

class PasswordChangeForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    newpassword  = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = Customer
        fields = ["username", "newpassword"]

    #def clean_newpass(self):
        #newpass = self.cleaned_data.get("newpassword")
        #x= Customer.objects.filter(newpassword=newpass)


class CheckoutForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ["ordered_by", "shipping_address", "email", 'payment_method']



class ChangeAddressForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    shipping_address = forms.CharField(widget = forms.TextInput)
    change_address = forms.CharField(widget = forms.TextInput)

    class Meta :
        model = Order
        fields = ["shipping_address", "change_address","username"]    

       
