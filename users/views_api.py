from django.contrib.auth.models import User
from rest_framework import generics, views
from . import serializers
from . import permissions


class UsersView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (permissions.IsOwner,)

    def get_object(self):
        return self.request.user

    def get_serializer(self, instance=None, data=None, many=False, partial=False):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return self.serializer_class(instance=instance, data=data, many=many, partial=True)
        elif self.request.method == "GET":
            return self.serializer_class(instance=instance, many=many, partial=partial)


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return views.Response(serializer.data, status=200)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (permissions.IsOwner,)

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(request.user)
            return views.Response(serializer.data, status=200)
