from django.contrib.auth.models import User
from rest_framework import generics
from . import serializers

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.UserListSerializer
        return serializers.UserCreateSerializer   
