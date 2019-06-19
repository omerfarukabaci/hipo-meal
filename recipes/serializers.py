from .models import Recipe, Ingredient
from rest_framework import serializers


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self._choices[obj]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name',)
        extra_kwargs = {
            'name': {'validators': []},
        }


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    difficulty = ChoiceField(choices=Recipe.DIFFICULTY_CHOICES)
    author = serializers.SerializerMethodField(source='get_author')
    date_posted = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('title', 'content', 'difficulty', 'ingredients',
                  'vote_points', 'vote_count', 'like_count', 'author', 'date_posted')

    def create(self, data):
        request = self.context.get("request")
        author = request.user
        recipe = Recipe(title=data["title"], content=data["content"],
                        author=author, difficulty=str(data["difficulty"]))
        recipe.save()
        for ingredient in data["ingredients"]:
            lookup_name = ingredient["name"].lower()
            lookup_name = lookup_name.replace(" ", "_")
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient["name"], lookup_name=lookup_name)
            recipe.ingredients.add(ingredient)

        return recipe

    def update(self, instance, data):
        if "ingredients" in data:
            new_ingredients = set()
            for ingredient in data["ingredients"]:
                lookup_name = ingredient["name"].lower()
                lookup_name = lookup_name.replace(" ", "_")
                ingredient, created = Ingredient.objects.get_or_create(name=ingredient["name"], lookup_name=lookup_name)
                new_ingredients.add(ingredient)

            current_ingredients = set(instance.ingredients.all())
            unchanging_ingredients = new_ingredients.intersection(current_ingredients)
            ingredients_to_add = new_ingredients.difference(unchanging_ingredients)
            ingredients_to_remove = current_ingredients.difference(unchanging_ingredients)

            for ingredient in ingredients_to_add:
                instance.ingredients.add(ingredient)

            for ingredient in ingredients_to_remove:
                instance.ingredients.remove(ingredient)

            data.pop("ingredients", None)

        super().update(instance, data)
        return instance

    def get_author(self, obj):
        return obj.author.username
