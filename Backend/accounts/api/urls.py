from django.urls import path,include
from .views import registration_view,UserList,ProfileDetail,ChangePasswordView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

app_name='accounts'

router=routers.SimpleRouter()
router.register('users',UserList)

urlpatterns = [
    path('',include(router.urls)),
    path('register/',registration_view,name='register'),
    path('login/',obtain_auth_token,name='login'),
    path('profile/',ProfileDetail.as_view(),name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
