from rest_framework import generics, views, permissions
from . import serializers


class UsersView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserDetailSerializer

    def get_object(self):
        return self.request.user


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return views.Response(serializer.data, status=200)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request.user)
        return views.Response(serializer.data, status=200)
