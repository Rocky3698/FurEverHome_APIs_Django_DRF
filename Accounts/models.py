from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .constants import ROLE_CHOICES

def is_valid_role(role)->bool:
    return role in ['admin','shelter','adopter']

class UserManager(BaseUserManager):
    def create_user(self, email, role, password=None,**extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not is_valid_role(role):
            raise ValueError('Invalid role')
        
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)

        return self.create_user(email,'admin',password,**extra_fields)

class User (AbstractBaseUser,PermissionsMixin):
    email                   = models.EmailField(unique=True)
    first_name              = models.CharField(max_length=50, blank=True, null=True)
    last_name               = models.CharField(max_length=50, blank=True, null=True)
    phone_number            = models.CharField(max_length=15, blank=True, null=True)
    profile_picture         = models.URLField(max_length=200, blank=True, null=True)
    bio                     = models.TextField(max_length=200, blank=True, null=True)
    role                    = models.CharField(max_length=10, choices=ROLE_CHOICES)

    is_active                   = models.BooleanField(default=True)
    is_staff                    = models.BooleanField(default=False)
    is_superuser                = models.BooleanField(default=False)
    date_joined                 = models.DateTimeField(auto_now_add=True)


    objects = UserManager()
    
    USERNAME_FIELD              = 'email'
    REQUIRED_FIELDS             = []

    class Meta:
        verbose_name            = 'User'
        verbose_name_plural     = 'Users'

    def __str__(self) -> str:
        return self.email
