from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Owner,Category,Product
from .forms import Ownerlogin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView 
from  django.urls import reverse_lazy
from customer.models import Cart
from django.db.models import Q
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    cat=Category.objects.all() 
    return render(request,'apple/home.html',{'category':cat})

def categorypage(request):
    cati=Category.objects.all()
    return render(request,'apple/categorypage.html',{'category':cati})
    
def product(request,pk):
    prod=Product.objects.filter(catid=pk)
    print(pk)
    if request.user.is_authenticated:
        item_already= []
        for i in prod:
            if Cart.objects.filter(Q(product=i.id) & Q(user=request.user)):
                item_already.append(i.name)
        print(item_already)
        return render(request,'apple/product.html',{'product':prod,"item_already":item_already})
    return render(request,'apple/product.html',{'product':prod})

def own_login(request):                         
    g=Ownerlogin(request.POST or None)          
    if g.is_valid():                           
        user=g.cleaned_data.get("owner")
        obj=Owner.objects.get(owner=user)
        request.session['user_log']={'name':obj.owner,"email":obj.password}
         
        return redirect("apple:owner")            
    return render(request,'apple/own_login.html',{"signin":g}) 
   

def owner(request):
    d=Product.objects.all()
    return render(request,"apple/owner.html",{'prods':d})



def logouts(request):
    request.session.pop("user_log") 
    return redirect("apple:home")  
   
class Addproduct(CreateView):
    template_name='apple/addproduct.html'
    model=Product
    fields=['name','desc','price','discount','image','stock','catid']
    context_object_name='form'
   
class Upproduct(UpdateView):
    template_name='apple/upproduct.html'
    model=Product
    fields=['name','desc','price','discount','image','stock','catid']
    context_object_name='form'


class Delproduct(DeleteView):
    
    template_name='apple/delproduct.html'
    model=Product
    context_object_name='form'
    success_url=reverse_lazy("apple:owner")
    success_message='product deleted'
