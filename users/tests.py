from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse


class UserLoginViewTestCase(APITestCase):
    def setUp(self):
        self.username = "test_user"
        self.password = "testuserpass123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token, created = Token.objects.get_or_create(user=self.user)

    def test_login_without_username(self):
        response = self.client.post(reverse("api-users:login"), data={"password": self.password})
        self.assertEqual(response.status_code, 400)

    def test_login_without_password(self):
        response = self.client.post(reverse("api-users:login"), data={"username": self.username})
        self.assertEqual(response.status_code, 400)

    def test_login_with_wrong_password(self):
        response = self.client.post(reverse("api-users:login"), data={"username": self.username,
                                                                      "password": "wrongpassword"})
        self.assertEqual(response.status_code, 400)

    def test_login_successfully(self):
        response = self.client.post(reverse("api-users:login"), data={"username": self.username,
                                                                      "password": self.password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['token'], self.token.key)


class UsersViewTestCase(APITestCase):
    def setUp(self):
        self.username = "test_user"
        self.password = "testuserpass123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token, created = Token.objects.get_or_create(user=self.user)

    def test_register_without_username(self):
        response = self.client.post(reverse("api-users:users"), data={"password": "testuser2pass123",
                                                                      "email": "test2@test.com"})
        self.assertEqual(response.status_code, 400)

    def test_register_without_password(self):
        response = self.client.post(reverse("api-users:users"), data={"username": "test_user2",
                                                                      "email": "test2@test.com"})
        self.assertEqual(response.status_code, 400)

    def test_register_without_email(self):
        response = self.client.post(reverse("api-users:users"), data={"username": "test_user2",
                                                                      "password": "testuser2pass123"})
        self.assertEqual(response.status_code, 201)

    def test_register_with_email(self):
        response = self.client.post(reverse("api-users:users"), data={"username": "test_user2",
                                                                      "password": "testuser2pass123",
                                                                      "email": "test2@test.com"})
        self.assertEqual(response.status_code, 201)

    def test_register_with_current_username(self):
        response = self.client.post(reverse("api-users:users"), data={"username": "test_user",
                                                                      "password": "testuser2pass123",
                                                                      "email": "test2@test.com"})
        self.assertEqual(response.status_code, 400)


class ChangePasswordViewTestCase(APITestCase):
    def setUp(self):
        self.username = "test_user"
        self.password = "testuserpass123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_change_password_with_wrong_old_password(self):
        response = self.client.post(reverse("api-users:change-password"), data={"old_password": "wrongpassword",
                                                                                "new_password": "newpassword123"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("wrong" in response.content.decode('utf-8').lower())

    def test_change_password_with_short_password(self):
        response = self.client.post(reverse("api-users:change-password"), data={"old_password": "testuserpass123",
                                                                                "new_password": "1234"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("short" in response.content.decode('utf-8').lower())

    def test_change_password_with_common_password(self):
        response = self.client.post(reverse("api-users:change-password"), data={"old_password": "testuserpass123",
                                                                                "new_password": "1234abcd"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("common" in response.content.decode('utf-8').lower())

    def test_change_password_with_numeric_password(self):
        response = self.client.post(reverse("api-users:change-password"), data={"old_password": "testuserpass123",
                                                                                "new_password": "06967464"})
        self.assertEqual(response.status_code, 400)
        self.assertTrue("numeric" in response.content.decode('utf-8').lower())

    def test_change_password_successfully(self):
        response = self.client.post(reverse("api-users:change-password"), data={"old_password": "testuserpass123",
                                                                                "new_password": "newpassword123"})
        self.assertEqual(response.status_code, 200)
