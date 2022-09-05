from django.contrib import messages
from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from apple.models import Product
from apple.views import product
from .models import Cart,OrderPlaced
from .forms import CReg,CLog,Cchangepass
from django.views import generic
from django.contrib.auth import login,logout,update_session_auth_hash,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import EditUserProfileForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.


class Register(generic.View):   
    def get(self,request): 
        return render(request,"customer/forms.html",{'form1':CReg(None)}) 
    def post(self,request):
        f=CReg(request.POST)
        if f.is_valid():
            data=f.save(commit=False)
            p=f.cleaned_data.get("password")  
            data.set_password(p)
            #data.password=p   # non encrypt password 
            data.save() 
            return HttpResponse("user created")
        return render(request,"customer/forms.html",{'form1':f})
        
# class LoginPage(generic.View):   
#     def get(self,request):  
#         return render(request,"customer/forms.html",{'form1':CLog(None)}) 
#     def post(self,request):
#         f=CLog(request.POST)
#         if f.is_valid():
#             u=f.cleaned_data.get('username')
#             p=f.cleaned_data.get("password")
#             #usr=User.objects.get(username=u,password=p)
#             usr = authenticate(username=u, password=p)
#             if usr:
#                 login(request,usr)  
#                 print(usr.username)
#             return redirect("apple:home")
#         return render(request,"customer/forms.html",{'form1':f})  

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("apple:home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="customer/forms.html", context={'form1':form})     

def clogout(request):
    logout(request) 
    return redirect("apple:home")  
   


#change Password with old password
# def user_change_pass(request):
#     if request.method =="POST":
#         fm=PasswordChangeForm(user=request.user,data=request.POST)
#         if fm.is_valid():
#             fm.save()
#             update_session_auth_hash(request,fm.user)
#             return HttpResponse("password changed")
#             #return redirect("apple:home")
#     else:
#         fm=PasswordChangeForm(user=request.user)
    
#     return render(request,'customer/cuschangepass.html',{'form1':fm})



@login_required
def cchangepass(request):
    g=Cchangepass(request.POST or None)          
    if g.is_valid():
        if request.user.is_authenticated:   
            ol=g.cleaned_data.get("oldpass")
            p1=g.cleaned_data.get("newpass")
            real=request.user.password  
            if ol!=real:
                messages.warning(request, "your old password is not correct!")
            else:
                usr=User.objects.get(username=request.user.username)
                usr.password=p1
                usr.save()
                update_session_auth_hash(request,usr) 
                messages.success(request, "your password has been changed successfuly.!")
        else:
            return HttpResponse("you are not log in")

            
    return render(request,'customer/cuschangepass.html',{"form1":g}) 





@login_required
def user_profile(request):
    if request.user.is_authenticated:
        if request.method =="POST":
            fm=EditUserProfileForm(request.POST, instance=request.user)
            if fm.is_valid():
                messages.success(request,'Profile UPdated !!!')
                fm.save()
        else:
            fm=EditUserProfileForm(instance=request.user)
        return render(request,'customer/customerprofile.html',{'name':request.user,'form':fm})
    else:
        return render('customer:c-signin')




#######################################################################################
#CART
@login_required
def add_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    print(product_id)
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
    if cart:
        cart_prod_total=[]
        for i in Cart.objects.all():
            if i.user==user:
                cart_prod_total.append(i.quantity * i.product.price)
        
        return render(request,'apple/addcart.html',{'carts':cart,'total':sum(cart_prod_total)})    

    else:
        return render(request,'apple/emptycart.html')

@login_required
def plus_cart(request):
    if request.method =='GET':
        pid=request.GET['prod_id']
        c=Cart.objects.get(Q(product=pid) & Q(user=request.user))
        c.quantity+=1
        c.save()

        cart_prod_total=[]
        for i in Cart.objects.all():
            if i.user==request.user:
                cart_prod_total.append(i.quantity * i.product.price)
        
        
        data={'quantity':c.quantity,'total':sum(cart_prod_total)}
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method =='GET':
        pid=request.GET['prod_id']
        c=Cart.objects.get(Q(product=pid) & Q(user=request.user))
        c.quantity-=1
        c.save()

        cart_prod_total=[]
        for i in Cart.objects.all():
            if i.user==request.user:
                cart_prod_total.append(i.quantity * i.product.price)
        
        
        data={'quantity':c.quantity,'total':sum(cart_prod_total)}
        return JsonResponse(data)

@login_required       
def remove_cart(request):
    if request.method =='GET':
        pid=request.GET['prod_id']
        c=Cart.objects.get(Q(product=pid) & Q(user=request.user))
        c.delete()

        cart_prod_total=[]
        for i in Cart.objects.all():
            if i.user==request.user:
                cart_prod_total.append(i.quantity * i.product.price)
        
        
        data={'total':sum(cart_prod_total)}
        return JsonResponse(data)

@login_required
def myoders(request):
    orders=OrderPlaced.objects.filter(user=request.user)
    if orders:
        my_order=[]
        for i in OrderPlaced.objects.all():
            if i.user==request.user:
                my_order.append(i)
        print(my_order)
        return render(request,'apple/orders.html',{'my_order':my_order})    

    else:
        return render(request,'apple/emptyoders.html')

@login_required
def payment_done(request):
    cart=Cart.objects.filter(user=request.user)
    for i in cart:
       OrderPlaced(user=i.user,product=i.product,quantity=i.quantity).save()
       i.delete()

    return redirect('/my_order')

    

        


        





   