from django import template
from ..models import Ingredient

register = template.Library()

@register.simple_tag
def get_top_ingredients():
    ingredients = Ingredient.objects.all()
    top_ingredients = list()
    for ingredient in ingredients:
        ingredient_usage_count = ingredient.recipe_set.all().count()
        top_ingredients.append({
            'name': ingredient.name,
            'count': ingredient_usage_count
        })
    top_ingredients_sorted = sorted(top_ingredients, key=lambda x:x['count'], reverse=True)
    return top_ingredients_sorted[:5]