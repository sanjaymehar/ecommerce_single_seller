
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms import fields
from django.contrib.auth.forms import UserChangeForm

class CReg(forms.ModelForm):   
   
    password=forms.CharField(widget=forms.PasswordInput)
    re_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','email','first_name','last_name']  
    def clean(self):
        super().clean()
        p=self.cleaned_data.get("password")
        p1=self.cleaned_data.get("re_password")
        if p!=p1:
            raise forms.ValidationError("Password did not match") 



class CLog(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        u=self.cleaned_data.get("username")   
        p=self.cleaned_data.get("password")    
        try:
            User.objects.get(username=u)
        except:
            raise forms.ValidationError("Username does not exist")
        try:
           User.objects.get(username=u,password=p) 

        except:
            raise forms.ValidationError(" password is not correct")

class Cchangepass(forms.Form):
    oldpass=forms.CharField(widget=forms.PasswordInput)
    newpass=forms.CharField(widget=forms.PasswordInput)
    confirm_new=forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        p1=self.cleaned_data.get("newpass")
        p2=self.cleaned_data.get("confirm_new")
        if p1!=p2:
            raise forms.ValidationError("password dont match")
        
           

class EditUserProfileForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','date_joined','last_login']

            

