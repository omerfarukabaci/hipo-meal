from rest_framework import generics, permissions
from . import serializers
from core import permissions as custom_permissions
from .models import Recipe


class RecipesView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RecipesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = (custom_permissions.IsOwnerOrReadOnly,)
