from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address!")
        if not password:
            raise ValueError("Users must have a password!")
        
        user_obj = self.model(
            email= self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

class User(AbstractBaseUser):
    email           = models.EmailField(max_length=255, unique=True)
    first_name      = models.CharField(max_length=255)
    last_name       = models.CharField(max_length=255)
    active          = models.BooleanField(default=True)
    staff           = models.BooleanField(default=False)
    admin           = models.BooleanField(default=False)
    created         = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD  = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email  
    
    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active



class Profile(models.Model):
    GENDER_CHOICE = (
        ('m', "Male"),
        ('f', "Female"),
        ('o', "Other"),
    )
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    confirm_email   = models.BooleanField(default=False)
    confirmed_date  = models.DateTimeField(blank=True, null=True)
    profile_pic     = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    gender          = models.CharField(max_length=1, choices=GENDER_CHOICE, blank=True)

    def __str__(self):
        return self.user.email
    
    def set_confirmed_date(self):
        self.confirmed_date = timezone.now()
        self.save()
    