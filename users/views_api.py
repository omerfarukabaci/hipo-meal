from rest_framework import generics, views
from . import serializers
from . import permissions


class UsersView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (permissions.IsOwner,)

    def get_object(self):
        return self.request.user


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return views.Response(serializer.data, status=200)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (permissions.IsOwner,)

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request.user)
        return views.Response(serializer.data, status=200)
