import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):

    def create_user(self, username, first_name, last_name, email, password=None):

        # validate username and email
        if not username:
            raise ValueError('Username must be provided')

        if not email:
            raise ValueError('email must be provided')

        user = self.model(
            username        = username,
            first_name      = first_name,
            last_name       = last_name,
            email           = self.normalize_email(email), # convert text cases to lowercase letters
        )
        # set user password
        user.set_password(password)

        # save new user
        user.save(using=self._db)
        return user

    def create_superuser(self,username, first_name, last_name, email, password):

        user = self.create_user(
            username        = username,
            first_name      = first_name,
            last_name       = last_name,
            email           = self.normalize_email(email),
            password        = password
        )

        user.is_admin = True
        user.is_superadmin = True
        user.is_staff = True
        user.is_active = True

        user.save(using=self._db)

        return user


class Account(AbstractBaseUser):
    id              = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )
    username        = models.CharField(max_length=30, unique=True) 
    first_name      = models.CharField(max_length=50) 
    last_name       = models.CharField(max_length=50)
    middle_name     = models.CharField(max_length=50, null=True, blank=True)
    email           = models.EmailField(unique=True)
    phone_number    = models.CharField(max_length=30, null=True, blank=True)

    # required fields from AbstractBaseUser model
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' # sign in with email instead of username
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True

