from django import forms
from django.contrib.auth.models import User
from .models import *

error = {
    'min_length':'tedad kam ast',
    'required':'elzam b por boudan',
}


class UserRegisterForm(forms.Form):
    user_name=forms.CharField(error_messages=error,max_length=200,widget=forms.TextInput(attrs={'placeholder':'نام کاربری خود را وارد نمایید'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'enter email...'}))
    first_name=forms.CharField(max_length=10,min_length=5,error_messages=error)
    last_name=forms.CharField(max_length=200)
    password_1=forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={'placeholder' : 'plz pass...'}))
    password_2=forms.CharField(max_length=200)

    def clean_user_name(self):
        user =self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('نام کاربری وارد شده تکراری است')
        return user

    def clean_email(self):
         email = self.cleaned_data['email']
         if User.objects.filter(email=email).exists():
             raise forms.ValidationError('emai tekrari ast')
         return email


    def clean_password_2(self):
        password1 = self.cleaned_data['password_1']
        password2 = self.cleaned_data['password_2']
        if password1 != password2 :
            raise forms.ValidationError('password not match')
        elif len(password2) < 8:
            raise forms.ValidationError('password is short')
        elif not any(x.isupper() for x in password2):
            raise forms.ValidationError('hadeaghal ....')

        return password1


class UserLoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()
    remember = forms.BooleanField(required=False,widget=forms.CheckboxInput())


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone','address','profile_image']


class PhoneForm(forms.Form):
    phone = forms.IntegerField()


class CodeForm(forms.Form):
    code = forms.IntegerField()













