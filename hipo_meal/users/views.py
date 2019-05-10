from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == "POST":
        registration_form = UserRegisterForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            username = registration_form.cleaned_data.get('username')
            messages.success(request, f'Welcome to our world {username}!')
            return redirect('recipes-home')

    else:
        registration_form = UserRegisterForm()
        
    context = {
        'registration_form': registration_form
    }
    return render(request, 'users/register.html', context)
