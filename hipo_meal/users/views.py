from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def register(request):
    registration_form = UserCreationForm()
    context = {
        'registration_form': registration_form
    }
    return render(request, 'users/register.html', context)
