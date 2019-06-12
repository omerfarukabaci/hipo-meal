import django.contrib.auth.password_validation as password_validation
from django.contrib.auth.models import User
from rest_framework import generics, views
from rest_framework.authtoken.models import Token
from . import serializers
from . import permissions


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.UserListSerializer
        return serializers.UserCreateSerializer


class UserRetrieveView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = (permissions.IsAuthenticatedAndOwner,)


class LoginView(views.APIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, **kwargs):
        try:
            user = User.objects.get(username=request.data["username"])
        except Exception:
            return views.Response(data="Not found.", status=404)

        if not user.check_password(request.data["password"]):
            return views.Response(data="Authentication failed.", status=400)

        token = Token.objects.get(user=user)
        data = {
            'token': token.key,
            'username': user.username
        }

        return views.Response(data=data, status=200)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticatedAndOwner,)

    def post(self, request, **kwargs):
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                password_validation.validate_password(serializer.data["new_password"])
            except Exception as e:
                return views.Response(data=e, status=400)
            if not request.user.check_password(serializer.data["old_password"]):
                return views.Response(data="Old password is incorrect.", status=400)
            serializer.save(request.user)
            return views.Response(serializer.data, status=200)
        return views.Response(serializer.errors, status=400)
