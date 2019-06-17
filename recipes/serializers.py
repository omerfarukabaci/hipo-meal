from django.core.exceptions import ObjectDoesNotExist
from .models import Recipe, Ingredient
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Recipe
        fields = ('title', 'content', 'vote_points', 'vote_count', 'like_count', 'difficulty', 'ingredients')

    def create(self, data):
        request = self.context.get("request")
        author = request.user
        recipe = Recipe(title=data["title"], content=data["content"],
                        author=author)
        recipe.save()
        for ingredient_name in data["ingredients"]:
            lookup_name = ingredient_name.lower()
            lookup_name = lookup_name.replace(" ", "_")
            try:
                ingredient = Ingredient.objects.get(lookup_name=lookup_name)
                recipe.ingredients.add(ingredient)
            except ObjectDoesNotExist:
                ingredient = Ingredient(name=ingredient_name, lookup_name=lookup_name)
                ingredient.save()
                recipe.ingredients.add(ingredient)

        recipe.save()
        return recipe

    def to_representation(self, data):
        ingredient_names = []
        for ingredient in data.ingredients.all():
            ingredient_names.append(ingredient.name)

        return {
            'title': data.title,
            'content': data.content,
            'ingredients': ingredient_names
        }
