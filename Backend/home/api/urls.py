from django.urls import path,include
from .views import contact

app_name='home'

urlpatterns = [
    path('contact/',contact,name='contact'),
]
