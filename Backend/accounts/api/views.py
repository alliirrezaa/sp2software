from rest_framework import status,mixins,generics
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.generics import ListAPIView,ListCreateAPIView
from ..models import Profile,User
from django.contrib.auth import get_user_model
from .serializers import RegistrationSerializer,ProfileSerializer,ChangePasswordSerializer,UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password

class UserList(ModelViewSet):
    queryset=get_user_model().objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAdminUser]

class AllProfiles(ModelViewSet):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[IsAdminUser]


@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer=RegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            user=serializer.save()
            data['response']='Successfully registerd a new user.'
            data['email']=user.email
            data['username']=user.username
            data['phone']=user.phone
            token=Token.objects.get(user=user).key
            data['token']=token
        else:
            data=serializer.errors
        return Response(data)

class ProfileDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'message': 'Password updated.',
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
