from rest_framework import generics, permissions
from . import serializers
from .models import Recipe


class RecipesView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
