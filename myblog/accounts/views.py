from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout, update_session_auth_hash
from django.http import HttpResponse

from django.db import models



# SignupUser

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("blog:list")
        
    form = UserCreationForm()
    context = {
        'form':form,
    }
    return render(request, 'account/signup.html', context)


# Login

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("blog:list")
    form = AuthenticationForm()
    
    context = {
        'form':form,
    }
    
    return render(request, 'account/login.html', context)

# Logout

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect("blog:list")
    

# Change Password

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('blog:list')
    else:
        form = PasswordChangeForm(user=request.user)
        
    context = {
        'form':form,
    }
    return render(request, 'account/change_password.html', context)

# Reset Paassword



