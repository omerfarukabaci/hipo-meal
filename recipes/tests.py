from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
import json


class RecipesViewTestCase(APITestCase):
    def setUp(self):
        self.username = "test_user"
        self.password = "testuserpass123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.recipe = {
            "title": "test_title",
            "content": "test_content",
            "ingredients": [
                {
                    "name": "test_ingredient1"
                },
                {
                    "name": "test_ingredient2"
                },
                {
                    "name": "test_ingredient3"
                }
            ],
            "difficulty": 1
        }

    def test_list_recipes_without_authorization(self):
        response = self.client.get(
            reverse("api-recipes:recipes")
        )
        self.assertEqual(response.status_code, 200)

    def test_create_recipe_without_authorization(self):
        response = self.client.post(
            reverse("api-recipes:recipes"),
            data=json.dumps(self.recipe),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

    def test_create_recipe_and_list_successfully(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            reverse("api-recipes:recipes"),
            data=json.dumps(self.recipe),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        created_recipe = json.loads(response.content)

        response = self.client.get(
            reverse("api-recipes:recipes")
        )
        recipe_list = json.loads(response.content)
        self.assertIn(created_recipe, recipe_list)

    def test_create_recipe_without_title(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.recipe.pop("title")
        response = self.client.post(
            reverse("api-recipes:recipes"),
            data=json.dumps(self.recipe),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_recipe_without_content(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.recipe.pop("content")
        response = self.client.post(
            reverse("api-recipes:recipes"),
            data=json.dumps(self.recipe),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_recipe_without_ingredients(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.recipe.pop("ingredients")
        response = self.client.post(
            reverse("api-recipes:recipes"),
            data=json.dumps(self.recipe),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
