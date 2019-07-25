from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Profile

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    password1   = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2   = forms.CharField(label='Password Confirm', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        pwrd1 = self.cleaned_data.get('password1')
        pwrd2 = self.cleaned_data.get('password2')
        if pwrd1 and pwrd2 and pwrd1!=pwrd2:
            raise forms.ValidationError("Passwords don't match!")
        return pwrd2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name','active', 'admin',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise forms.ValidationError("Email and password don't match! Note: both are case-sensitive!")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password?")
            if not user.is_active:
                raise forms.ValidationError("User is not active, Confirm email or contact us!")
            return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    email     = forms.EmailField(help_text='Required. Inform a valid email address')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

    def clean_email(self):
        email   = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Sorry, this email is already taken!!!")
        return email
    
    def clean_password2(self):
        pwrd1 = self.cleaned_data.get('password1')
        pwrd2 = self.cleaned_data.get('password2')
        if pwrd1 and pwrd2 and pwrd1!=pwrd2:
            raise forms.ValidationError("Passwords don't match!")
        return pwrd2

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

class UserProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic','gender',)