from django import forms
from django.core.exceptions import ValidationError

from .models import Owner

class Ownerlogin(forms.Form):                               
    owner=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput) 
    def clean(self):
        ow=self.cleaned_data.get("owner")
        passw=self.cleaned_data.get("password")
        try:
            ow=Owner.objects.get(owner=ow)   
        except:
            raise forms.ValidationError("owner name doesnot exists")
        else:
            if not Owner.objects.filter(owner=ow,password=passw):
                raise ValidationError("password doesnot match")

      