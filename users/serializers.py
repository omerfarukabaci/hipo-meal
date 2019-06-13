import django.contrib.auth.password_validation as password_validation
from django.contrib.auth.models import User
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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError(detail=e.args[0])
        return value

    def validate(self, data):
        user = User.objects.get(username=data["username"])
        if not user.check_password(data["password"]):
            raise serializers.ValidationError(detail="Wrong password.")

        token, created = Token.objects.get_or_create(user=data["user"])
        data["user"] = user
        data["token"] = token
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
        user.set_password(self.data["new_password"])
        user.save()

    def validate_old_password(self, value):
        request = self.context.get("request")
        user = request.user
        if not user.check_password(value):
            raise serializers.ValidationError(detail="Wrong password.")

        return value
