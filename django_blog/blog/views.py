from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from .models import Post




def home(request):
    posts = Post.objects.all().order_by('-published_date')
    # Create a context dictionary to pass the data to the template
    context = {
        'posts': posts
    }
    # Render the home template with the posts data
    return render(request, 'blog/home.html', context)


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


@login_required
def edit_profile(request):
    """
    Handles user profile editing and profile picture uploads.
    """
    if request.method == 'POST':
        # Create form instances with submitted data and the current user's instances
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was updated successfully!')
            # Redirect to the homepage after successful edit
            return redirect('home')
    else:
        # For a GET request, create form instances with the current user's data
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'blog/edit_profile.html', context)
