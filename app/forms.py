from django import forms
from.models import *
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
class SignupForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'password', 'password_again']
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password_again' : forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter password'}),
        }
    
    def clean(self):
        data = self.cleaned_data
        username = data.get('username')
        password = data.get('password')
        password_again = data.get('password_again')

        customer = Customer.objects.filter(username=username)

        if customer.exists():
            raise forms.ValidationError("A user with this name already exists")

        if password != password_again:
            raise forms.ValidationError("Passwords do not match.")
        
        if len(password) < 12:
            raise forms.ValidationError("Password is too short.")
        
        if len(password) > 20:
            raise forms.ValidationError("Password is too long.")
        
        uppercase = "QWERTYUIOPASDFGHJKLZXCVBNM"
        lowercase = "qwertyuiopasdfghjklzxcvbnm"
        numbers = "1234567890"
        symbols = "!$%&*"

        upper = False
        lower = False
        num = False
        symb = False

        for c in uppercase:
            if c in password:
                upper = True
                break
        
        if not upper:
            raise forms.ValidationError("Password must contain an uppercase letter.")

        for c in lowercase:
            if c in password:
                lower = True
                break
        
        if not lower:
            raise forms.ValidationError("Password must contain a lowercase letter.")
        
        for c in numbers:
            if c in password:
                num = True
                break
        if not numbers:
            raise forms.ValidationError("Password must contain a number.")
        
        for c in symbols:
            if c in password:
                symb = True
                break
        
        if not symb:
            raise forms.ValidationError("Password must contain a sybol ! $ % & or *")
        

        return data

class LoginForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["username", "password"]
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            }
    
    def clean(self):
        data = self.cleaned_data
        username = data.get("username")
        password = data.get("password")
        customer = Customer.objects.filter(username=username, password=password)

        if len(customer) == 0:
            raise forms.ValidationError("No Customer registered with this username and password")
        
        
        return data

class CreatePizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = [
            "size",
            "crust",
            "sauce",
            "cheese",
            "pepperoni",
            "chicken",
            "ham",
            "pineapple",
            "peppers",
            "mushrooms",
            "onions",
        ]


class OrderPizzaForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'address', 'card_number', 'expiration_date', 'ccv']
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'address' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Address'}),
            'card_number' : forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Card Number'}),
            'expiration_date' : forms.TextInput(attrs={'class':'form-control', 'placeholder' :' Expiration Date'}),
            'ccv' : forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'CCV'})
            }
    
    def clean(self):
        data = self.cleaned_data
        number = data.get("card_number")
        nums = "1234567890"
        for n in number:
            if n not in nums:
                raise forms.ValidationError("invalid Card Number")
        if len(number) != 16:
            raise forms.ValidationError("Invalid Card Number")
        
        ccv = data.get("ccv")

        for n in ccv:
            if n not in nums:
                raise forms.ValidationError("Invalid CCV")
        if len(ccv) != 3:
            raise forms.ValidationError("Invalid CCV")
        
        exp = data.get("expiration_date")
        if len(exp) < 4:
            raise forms.ValidationError("Invalid Expiration Date")
        qualify = "1234567890/"
        for c in exp:
            if c not in qualify:
                raise forms.ValidationError("Invalid Expiration Date")
        
        if len(exp) == 4:
            if exp[1] != "/":
                raise forms.ValidationError("Invalid Expiration Date")
        
        if len(exp) == 5:
            if exp[2] != "/":
                raise forms.ValidationError("Invalid Expiraton Date")
        
        return data