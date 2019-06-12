from django.contrib.auth.models import User
from rest_framework import generics, views
from rest_framework.authtoken.models import Token
from . import serializers
from . import permissions


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (permissions.IsOwner,)

    def get_serializer(self, instance=None, data=None, many=False, partial=False):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return self.serializer_class(instance=instance, data=data, many=many, partial=True)
        elif self.request.method == "GET":
            return self.serializer_class(instance=instance, many=many, partial=partial)


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
    permission_classes = (permissions.IsOwner,)

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(request.user)
            return views.Response(serializer.data, status=200)
        return views.Response(serializer.errors, status=400)
