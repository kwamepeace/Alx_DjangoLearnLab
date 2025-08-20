from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, CustomUserCreationForm



def home(request):
    """
    Handle the home page view.
    """
    return render(request, 'blog/home.html')


def posts(request):
    """
    Handle the blog posts page view.
    """
    return render(request, 'blog/posts.html')

"""
view for handling user registration and login."""
def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'blog/register.html', {'form': form})


def login_view(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    context = {
        'form': form
    }
    return render(request, 'blog/login.html', context)



@login_required
def logout_view(request):
    """
    Handle user logout and redirect to homepage.
    """
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')