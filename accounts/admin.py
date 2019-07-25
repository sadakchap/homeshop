from django.contrib import admin
from .models import UserProfile
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm, UserAdminChangeForm
# Register your models here.
User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ['email', 'first_name', 'last_name', 'active', 'admin', 'created']
    list_filter  = ['active', 'staff', 'admin', 'created']
    search_fields = ['email', 'first_name', 'last_name']
    fieldsets = (
        ('None',{'fields':('email','password',)}),
        ('Personal Information', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)}
        ),
    )
    ordering = ('email',)
    filter_horizontal = ()
    

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'confirm_email', 'confirmed_date', 'gender',]
    list_filter = ['confirm_email', 'gender']
    # search_fields = ['user_id']
# admin.site.register(UserProfile)

# admin.site.register(User)
# admin.site.unregister(Group)
