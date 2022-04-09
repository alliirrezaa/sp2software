from rest_framework import serializers
from ..models import Profile,User
from django.contrib.auth import get_user_model, logout
from django.contrib import auth

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields='__all__'
        
class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=get_user_model()
        fields=['email','username','phone','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def save(self):
        user=User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            phone=self.validated_data['phone'],
        )

        password1=self.validated_data['password']
        password2=self.validated_data['password2']

        if password1 != password2:
            raise serializers.ValidationError({'password':'password must match!'})
        user.set_password(password2)
        user.save()
        return user


class ProfileHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','phone']


class ProfileSerializer(serializers.ModelSerializer):
    user=ProfileHelperSerializer()
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    address=serializers.CharField()
    class Meta:
        model=Profile
        fields=['user','first_name','last_name','address']

    def update(self, instance, validated_data):
        request = self.context.get("request")
        #get new data
        new_username=validated_data['user']['username']
        new_phone=validated_data['user']['phone']
        new_first_name = validated_data['first_name']
        new_last_name = validated_data['last_name']
        new_address= validated_data['address']
        #update User data
        user = request.user
        user.username=new_username
        user.phone=new_phone
        user.save()
        #update Profile data
        instance.first_name =new_first_name
        instance.last_name = new_last_name
        instance.address=new_address
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    