from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient
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


class RecipesDetailViewTestCase(APITestCase):
    def setUp(self):
        self.username = "test_user"
        self.password = "testuserpass123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.username2 = "test_user2"
        self.password2 = "testuserpass123"
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2)
        self.token2, created = Token.objects.get_or_create(user=self.user2)
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
        self.updated_recipe = {
            "title": "test_title_updated",
            "content": "test_content_updated",
            "ingredients": [
                {
                    "name": "test_ingredient1_updated"
                },
                {
                    "name": "test_ingredient2_updated"
                },
                {
                    "name": "test_ingredient3_updated"
                }
            ],
            "difficulty": 2
        }
        self.current_recipe = Recipe(title=self.recipe["title"], content=self.recipe["content"],
                                     author=self.user, difficulty=str(self.recipe["difficulty"]))
        self.current_recipe.save()
        for ingredient in self.recipe["ingredients"]:
            lookup_name = ingredient["name"].lower()
            lookup_name = lookup_name.replace(" ", "_")
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient["name"], lookup_name=lookup_name)
            self.current_recipe.ingredients.add(ingredient)

    def test_update_recipe_without_authorization(self):
        response = self.client.put(
            reverse("api-recipes:recipes-detail", args=[str(self.current_recipe.id)]),
            data=json.dumps(self.updated_recipe),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

    def test_update_recipe_with_authorization_by_other(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.put(
            reverse("api-recipes:recipes-detail", args=[str(self.current_recipe.id)]),
            data=json.dumps(self.updated_recipe),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_update_recipe_with_authorization_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(
            reverse("api-recipes:recipes-detail", args=[str(self.current_recipe.id)]),
            data=json.dumps(self.updated_recipe),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_partial_update_recipe_with_authorization_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.updated_recipe.pop("title")
        self.updated_recipe.pop("difficulty")
        response = self.client.patch(
            reverse("api-recipes:recipes-detail", args=[str(self.current_recipe.id)]),
            data=json.dumps(self.updated_recipe),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_recipe_without_authorization(self):
        response = self.client.delete(
            reverse("api-recipes:recipes-detail", args=[str(self.current_recipe.id)])
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_recipe_with_authorization_by_other(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = self.client.delete(
            reverse("api-recipes:recipes-detail", args=[str(self.current_recipe.id)])
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_recipe_with_authorization_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(
            reverse("api-recipes:recipes-detail", args=[str(self.current_recipe.id)])
        )
        self.assertEqual(response.status_code, 204)

    def test_recipe_detail_without_authorization(self):
        response = self.client.get(
            reverse("api-recipes:recipes-detail", args=[str(self.current_recipe.id)])
        )
        self.assertEqual(response.status_code, 200)
