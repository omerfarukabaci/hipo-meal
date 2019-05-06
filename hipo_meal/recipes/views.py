from django.shortcuts import render
from .models import Recipe

def home(request):
    context = {
        'recipes': Recipe.objects.all()
    }
    return render(request, 'recipes/home.html', context)
