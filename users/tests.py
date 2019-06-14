from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse


class UserLoginViewTestCase(APITestCase):
    def setUp(self):
        self.username = "test_user"
        self.email = "test_user@test.com"
        self.password = "testuserpass123"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token, created = Token.objects.get_or_create(user=self.user)

    def test_login_without_username(self):
        response = self.client.post(reverse("api-login"), data={"password": self.password})
        self.assertEqual(response.status_code, 400)

    def test_login_without_password(self):
        response = self.client.post(reverse("api-login"), data={"username": self.username})
        self.assertEqual(response.status_code, 400)

    def test_login_with_wrong_password(self):
        response = self.client.post(reverse("api-login"), data={"username": self.username,
                                                                "password": "wrongpassword"})
        self.assertEqual(response.status_code, 400)

    def test_login_successfully(self):
        response = self.client.post(reverse("api-login"), data={"username": self.username,
                                                                "password": self.password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['token'], self.token.key)
