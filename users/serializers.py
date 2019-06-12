import django.contrib.auth.password_validation as password_validation
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username',)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


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

        data["user"] = user
        return data

    def to_representation(self, data):
        token = Token.objects.get(user=data["user"])
        return {
            'username': data["username"],
            'token': token.key
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def save(self, user):
        user.set_password(self.data["new_password"])
        user.save()

    def validate_new_password(self, value):
        try:
            password_validation.validate_password(value)
        except Exception as e:
            raise serializers.ValidationError(detail=e.messages)

        return value

    def validate_old_password(self, value):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if not user.check_password(value):
            raise serializers.ValidationError(detail="Wrong password.")

        return value
