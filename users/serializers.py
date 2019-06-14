import django.contrib.auth.password_validation as password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def create(self, data):
        user = User(username=data["username"])
        user.set_password(data["password"])

        if "email" in data:
            user.email = data["email"]

        user.save()
        Token.objects.create(user=user)
        return user

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        try:
            user = User.objects.get(username=data["username"])
        except ObjectDoesNotExist:
            raise serializers.ValidationError(detail={"username": "User does not exist."})

        if not user.check_password(data["password"]):
            raise serializers.ValidationError(detail={"password": "Wrong password."})

        token, created = Token.objects.get_or_create(user=user)
        data["user"] = user
        data["token"] = token.key
        return data

    def to_representation(self, data):
        return {
            'username': data["username"],
            'token': data["token"]
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[password_validation.validate_password])

    def save(self, user):
        user.set_password(self.validated_data["new_password"])
        user.save()

    def validate_old_password(self, value):
        request = self.context.get("request")
        user = request.user
        if not user.check_password(value):
            raise serializers.ValidationError(detail="Wrong password.")

        return value
