from django.contrib.auth.models import User
from rest_framework import generics, views
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
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
        except:
            return views.Response(data="User is not found.", status=404)
        
        if not user.check_password(request.data["password"]):
            return views.Response(data="Authentication failed.", status=400)

        token = Token.objects.get(user=user)
        data = {
            'token': token.key,
            'username': user.username
        }

        return views.Response(data=data, status=200)