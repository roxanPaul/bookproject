from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout



# Create your views here.

def register_user(request):
    if request.method=="POST":
        username=request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1==password2:


            if User.objects.filter(email=email).exists():
                messages.info(request,'this mail already taken')
            else:
                user=User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name)
                user.save()
            return redirect('login')
        else:
            messages.info(request,'This password not matching')
        return redirect('register')
    return render(request, 'auth/register.html')

def login_user(request):


    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return render(request,'user/list.html')
        else:
            messages.info(request,'please provide correct details')
            return redirect('login')
    return render(request,'auth/login.html')
def logout(request):
    auth.logout(request)
    messages.info(request,'you may logout')
    return redirect('login')

def HomePage(request):
    return render(request,'auth/home.html')
