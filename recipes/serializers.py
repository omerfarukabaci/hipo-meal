from .models import Recipe, Ingredient, User
from rest_framework import serializers
from pytz import timezone


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.ListField(child=serializers.CharField())
    difficulty = serializers.IntegerField(min_value=1, max_value=4)

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
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name, lookup_name=lookup_name)
            recipe.ingredients.add(ingredient)

        recipe.difficulty = str(data["difficulty"])
        recipe.save()
        return recipe

    def to_representation(self, data):
        ingredient_names = []
        for ingredient in data.ingredients.all():
            ingredient_names.append(ingredient.name)

        return {
            'title': data.title,
            'content': data.content,
            'difficulty': data.get_difficulty_display(),
            'ingredients': ingredient_names,
            'likes': data.like_count,
            'votes': data.vote_points / data.vote_count if data.vote_count else 0,
            'author': User.objects.get(id=data.author_id).username,
            'date_posted': data.date_posted.astimezone(timezone('Europe/Istanbul')).strftime("%Y-%m-%d %H:%M")
        }
