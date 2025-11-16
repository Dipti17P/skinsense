from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def index(request):
    # If the user is already authenticated, send them to the dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/index.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz_start')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
