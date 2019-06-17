from .models import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('title', 'content', 'author', 'vote_points', 'vote_count', 'like_count', 'difficulty', 'ingredients')
