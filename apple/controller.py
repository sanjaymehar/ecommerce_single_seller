from django.http import request
from django.urls import path
from . import views
from customer import views as cust

app_name='apple'
#app_name='customer'
urlpatterns = [
    path("own_login/",views.own_login,name='own_login'),
    path("owner/",views.owner,name='owner'),
    path("addproduct/",views.Addproduct.as_view(),name="addproduct"),
    path("upproduct/<int:pk>",views.Upproduct.as_view(),name="updateproduct"),
    path("delproduct/<int:pk>",views.Delproduct.as_view(),name="deleteproduct"),
    path("logout/",views.logouts,name='signout'),
    path("",views.home,name="home"),
    path('add-to-cart/',cust.add_cart,name='add-to-cart'),
    path('cart/',cust.show_cart,name='showcart'),
    path('pluscart/',cust.plus_cart),
    path('minuscart/',cust.minus_cart),
    path('removecart/',cust.remove_cart),
    path('paymentdone/',cust.payment_done),
    path('my_order/',cust.myoders,name='my_order'),
    
    
]
