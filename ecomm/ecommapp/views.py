from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from .forms import UserRegister,UserLogin,CartForm,OrderForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecommapp.models import Products,Carts,Orders
from django.core.mail import send_mail,settings

# Create your views here.

class Home(View):
    
    def get(self,request,*args,**kwargs):
        data=Products.objects.all()
        return render(request,'index.html',{'products':data})
    
class RegView(View):
    def get(self,request,*args,**kwargs):
       form=UserRegister()
       return render(request,'regform.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        # first=request.POST.get('first_name')
        # last=request.POST.get('last_name')
        # username=request.POST.get('username')
        # password=request.POST.get('password')
        # email=request.POST.get('email')
        form=UserRegister(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,'registration successfull')
            return HttpResponse('success')
        else:
            messages.error(request,'invalid')
            return redirect('log_view')
        
class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=UserLogin()
        return render(request,'userlogin.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=UserLogin(request.POST)
    
        uname=request.POST.get('username')
        passw=request.POST.get('password')
        user=authenticate(request,username=uname,password=passw)
        if user:
            login(request,user)
            messages.success(request,'login successfull')
            return redirect('home_view')
        else:
            messages.error(request,'invalid')
            return redirect('log_view')
        
class LogoutView(View):
      def get(self,request,*args,**kwargs):
          logout(request)
          messages.success(request,'logout successfull')
          return redirect('home_view')
      
class ProductDetailview(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        product=Products.objects.get(id=id)
        return render(request,'productdetail.html',{'product':product})
    
class AddTocartView(View):
    def get(self,request,*args,**kwargs):
                form=CartForm()
                id=kwargs.get('id')
                product=Products.objects.get(id=id)
                return render(request,'addtocart.html',{'form':form,'product':product})
    
    def post(self,request,*args,**kwargs):
            id=kwargs.get('id')
            product=Products.objects.get(id=id)
            user=request.user
            quantity=request.POST.get('quantity')
            Carts.objects.create(product=product,user=user,quantity=quantity)
            return redirect('home_view')
    
class CartListView(View):
    def get(self,request,*args,**kwargs):
    
        cart=Carts.objects.filter(user=request.user).exclude(status='order_placed')
        return render(request,'cartlistview.html',{'cart':cart}) 
    
class placeOrderView(View):
     def get(self,request,*args,**kwargs):
          form=OrderForm()
          return render(request,'place-order.html',{'form':form}) 

     def post(self,request,*args,**kwargs):
        cart_id=kwargs.get('cart_id')
        cart=Carts.objects.get(id=cart_id)
        user=request.user
        address=request.POST.get('address')
        email=request.POST.get('email')
        Orders.objects.create(user=user,cart=cart,address=address,email=email)
        send_mail('confirmation','order placed successfully!',settings.EMAIL_HOST_USER,[email])
        cart.status='order_placed'
        cart.save()
        return redirect('home_view')

class CartDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        data=Carts.objects.get(id=id)
        data.delete()
        return redirect('cartlist_view')

          
     


     

         



        
       
    

    

    

