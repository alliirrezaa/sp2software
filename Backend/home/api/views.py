from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import EmailMessage
from .serializers import ContactSerializer
from rest_framework import status,mixins,generics
from rest_framework.views import APIView

"""@api_view(['POST',])
def contact(request):
    if request.method == 'POST':
        serializer=ContactSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            data['subject']=serializer['subject']
            data['email']=serializer['email']
            data['msg']=serializer['message']
            body=msg
            form=EmailMessage('contact us',body,'test',('software.proj.test@gmail.com',))
            form.send(fail_silently=False)
    return Response(data)
"""
@api_view(['POST',])
def contact(request):
    if request.method == 'POST':
        serializer=ContactSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            data['subject']=request.data['subject']
            data['email']=request.data['email']
            data['message']=request.data['message']
            body= data['subject']+' \n'+data['email']+' \n'+data['message']
            form=EmailMessage('contact us',body,'test',('software.proj.test@gmail.com',))
            form.send(fail_silently=False)
    return Response(data)