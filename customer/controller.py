from django.http import request
from django.urls import path
from . import views

app_name='customer'
#app_name='apple'

urlpatterns = [
    #path("",views.Home.as_view(),name='main'),
    path("custsignup/",views.Register.as_view(),name='c-signup'),
    #path("custsignin/",views.LoginPage.as_view(),name='c-signin'),
    path("custlogout/",views.clogout,name='clogout'),
    path('custpasschange/',views.cchangepass,name='c-changepass'),
    path('custprofile/',views.user_profile,name='c-profile'),
    path("custsignin/", views.login_request, name="c-signin")
    
    
]
