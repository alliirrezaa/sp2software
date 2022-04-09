from django.contrib import admin
from .models import User
from .forms import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

class UserAdmin(BaseUserAdmin):
    form=UserChangeForm
    add_form=UserCreateForm
    list_display=('email','username','phone')
    list_filter=('email','is_active')
    fieldsets = (
        ('user',{'fields':('email','password')}),
        ('Personal info',{'fields':('is_admin',)}),
        ('Permissions',{'fields':('is_active',)})
    )
    
    add_fieldsets = (
       (None,{'fields':('email','username','phone','password1','password2')}),
    )
    search_fields=('email',)
    ordering=('email',)
    filter_horizontal=()


admin.site.register(User,UserAdmin)
admin.site.unregister(Group)