from django.contrib import admin
from .models import Recipe, Evaluation, Ingredient

admin.site.register(Recipe)
admin.site.register(Evaluation)
admin.site.register(Ingredient)
