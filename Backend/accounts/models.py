from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.core.mail import send_mail  
from django.urls import reverse

class UserManager(BaseUserManager):
    def create_user(self,email,username,phone,password):
        if not email:
            raise ValueError('please check email.')
        if not username:
            raise ValueError('please check username.')
        if not phone:
            raise ValueError('please check phone.')
        
        user=self.model(email=self.normalize_email(email),username=username,phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,phone,password):
        user=self.create_user(email,username,phone,password)
        user.is_admin=True
        user.save(using=self._db)
        return user

        
class User(AbstractBaseUser):
    username=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    phone=models.IntegerField()
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','phone']
    objects=UserManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True
    
    def has_module_perms(self,app_lable):
        return True

    @property
    def is_staff(self):
        return self.is_admin


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)

class Profile(models.Model):
    user=models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    address=models.TextField()

    def __str__(self):
        return self.user.email

@receiver(post_save,sender=User)
def create_Profile(sender,instance=None,created=False,**kwargs):
    if created:
        Profile.objects.create(user=instance)

