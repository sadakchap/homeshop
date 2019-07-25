from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.utils.http import is_safe_url
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm, UserChangeForm, UserProfileChangeForm

from django.utils.encoding import force_text
from django.contrib.auth import get_user_model

User = get_user_model()

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

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

def register(request):
    form = UserRegisterForm(request.POST or None)
    # next_ = request.GET.get('next')
    # next_post = request.POST.get('next')
    # redirect_path = next_ or next_post or None
    if form.is_valid():
        # email  = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password2')
        user = form.save(commit=False)
        user.set_password(password)
        user.active = False
        user.save()
        current_site = get_current_site(request)
        subject = 'Activate Your HomeShop Account'
        message = render_to_string(
            'account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        return redirect('account_activation_sent')
        # new_user = authenticate(username=email, password=password)
        # if user:
        #     login(request, new_user)
        #     messages.success(request,f"An account has been created with {email}")
        #     if is_safe_url(redirect_path, request.get_host()):
        #         return redirect(redirect_path)
        #     return redirect('/')
    return render(request, "accounts/register.html", {'form':form})

def home(request):
    return render(request, "home.html", {})

def account_activation_sent(request):
    return render(request, "accounts/account_activation_sent.html", {})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        user.profile.confirm_email = True
        user.profile.set_confirmed_date()
        user.save()
        login(request, user)
        messages.success(request, "Your account has been activated!")
        return redirect('complete_registration')
    else:
        return render(request, 'account_activation_invalid.html')

@login_required
def complete_registration(request):
    user = request.user
    u_form = UserChangeForm(request.POST or None, instance=user)
    p_form = UserProfileChangeForm(request.POST or None, request.FILES or None, instance=user.profile)
    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        return redirect('/')
    return render(request, 'accounts/complete_registration.html', {'u_form':u_form, 'p_form': p_form})
