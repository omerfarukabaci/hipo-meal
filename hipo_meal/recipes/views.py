from django.shortcuts import render

dummy_recipe_data = [
    {
        'title': 'Musakka',
        'image': '',
        'content': 'Please deal with your meal kind.',
        'post_date': '06/05/2019',
        'vote_point': '3.5/5',
        'vote_count': 13,
        'like_count': 5,
        'author': 'Ömer Faruk Abacı'
    },
    {
        'title': 'Pan Seared Salmon',
        'image': '',
        'content': 'Please deal with your meal kind.',
        'post_date': '06/05/2019',
        'vote_point': '5/5',
        'vote_count': 2,
        'like_count': 0,
        'author': 'Ömer Faruk Abacı 2'
    }
]

def home(request):
    context = {
        'recipes': dummy_recipe_data
    }
    return render(request, 'recipes/home.html', context)
