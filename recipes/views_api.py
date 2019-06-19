from rest_framework import generics, permissions, views
from . import serializers
from core import permissions as custom_permissions
from .models import Recipe


class RecipesView(generics.ListCreateAPIView):
    serializer_class = serializers.RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Recipe.objects.filter(is_hidden=False)


class RecipesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.RecipeSerializer
    permission_classes = (custom_permissions.IsOwnerOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_hidden = True
        instance.save()
        return views.Response(status=204)

    def get_queryset(self):
        return Recipe.objects.filter(is_hidden=False)
