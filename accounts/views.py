from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.utils.http import is_safe_url
from django.contrib import messages
from .forms import UserLoginForm, UserRegisterForm
# Create your views here.


def login_view(request):
    form = UserLoginForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if user:
            messages.success(request, f"You are Logged in as {email}")
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            return redirect("/")
    return render(request, "accounts/login.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def register(request):
    form = UserRegisterForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email  = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password2')
        user = form.save(commit=False)
        user.set_password(password)
        user.save()
        new_user = authenticate(username=email, password=password)
        if user:
            login(request, new_user)
            messages.success(request,f"An account has been created with {email}")
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            return redirect('/')
    return render(request, "accounts/register.html", {'form':form})

def home(request):
    return render(request, "home.html", {})