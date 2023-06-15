
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import login as loginn
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

# verification email
from .models import User_otp
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re
from django.core.exceptions import ValidationError


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    return render(request, 'index.html')

def shop(request):
    categories = Category.objects.filter(is_listed=False)
    context = {'categories': categories}
    return render(request, 'categories.html', context)

def collectionsview(request,slug):
    if Category.objects.filter(slug=slug).exists():
        products = Product.objects.filter(category__slug=slug)
        print("products are",products)
        category = Category.objects.filter(slug=slug).first()
        context = {'products':products,'category':category}
        return render(request,"products/index.html",context)
    else:
        messages.warning(request,"No such category found")
        return redirect('shop')
    

def productview(request, cate_slug, prod_slug):
    try:
        category = Category.objects.get(slug=cate_slug)
        product = Product.objects.get(slug=prod_slug)
    except Category.DoesNotExist:
        messages.error(request, "No such category found")
        return redirect('shop')
    except Product.DoesNotExist:
        messages.error(request, "No such product found")
        return redirect('shop')

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        size = request.POST.get('size')

    context = {
        'category': category,
        'product': product
    }

    return render(request, 'products/view.html', context)


def loginn(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('userlist')
        else:
            return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']

        if username.strip() == '' or password.strip() == '':
            messages.error(request, "Fields can't be blank!!!")
            return redirect('loginn')
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    auth.login(request,user)
                    return redirect('userlist')
                else:
                    auth.login(request,user)
                    return redirect('/')
            else:
                messages.error(request, "Username or Password Incorrect!!")
                return redirect('loginn')

    return render(request, 'login.html')



def register(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp:
            email = request.POST.get('email')
            usr = User.objects.get(email = email)
            if int(otp)== User_otp.objects.filter(user = usr).last().otp:
                usr.is_active = True
                usr.save()
                auth.login(request,usr)
                messages.success(request,f'Account is created for {usr.username}')
                User_otp.objects.filter(user = usr).delete()
                return redirect('index')
            else:
                messages.error(request,'Invalid OTP')
                return render(request,'register.html',{'otp':True,'usr':usr})
        else:
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['pass']
            password2 = request.POST['pass1']

            if username.strip() == '' or password1.strip() == '' or password2.strip() == '':
                messages.error(request, "Fields can't be blank!!!")
                return redirect('register')

            if password1 != password2:
                messages.error(request, "Passwords don't match!!")
                return redirect('register')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('register')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.is_superuser = False  
                user.is_active = False
                user.save()
                user_otp = random.randint(100000,999999)
                User_otp.objects.create(user=user, otp=user_otp)
                mess=f'Hey\t{user.username}!,\nOTP to verify your account for VIOLET is {user_otp}\n'
                send_mail(
                        "VIOLET: Validate Your Email and Dive In",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False
                    )
                messages.success(request, 'Please enter your OTP')
                return render(request,'register.html',{'otp':True,'usr':user})
                
                

    return render(request, 'register.html')

from django.shortcuts import render


def user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        username = user.username
        email = user.email
        return render(request, 'user_profile.html', {'username': username, 'email': email})
    else:
        return redirect('login')  

def logout(request):
    auth.logout(request)
    return redirect('/')












