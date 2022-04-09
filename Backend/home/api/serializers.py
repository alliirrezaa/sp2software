from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    subject=serializers.CharField(max_length=20)
    email=serializers.EmailField(max_length=20)
    message=serializers.CharField(max_length=20)
    