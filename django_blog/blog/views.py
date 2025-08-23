from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm, CommentForm
from django.views.generic.edit import FormMixin
from .models import Post, Comment
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
) 

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse,reverse_lazy




def home(request):
    posts = Post.objects.all().order_by('-published_date')
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


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


class BlogsView (ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    ordering = ['-published_date']


class BlogCreateView(CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('posts')


    # This method is overridden to set the author of the post to the current logged-in user before saving the form.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class BlogUpdateView (LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

# This test_func() checks if the current loggged-in user is the author of the post they are trying to update.
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

class BlogDeleteView (LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

"""
Views for handling comments on blog posts.

"""

class BlogDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    # Dynamically generate the success URL to redirect to the same post detail page after a comment is added
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.get_object().pk})


    # Passing additional context data to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the comment form and all comments for this post to the context
        context['form'] = self.get_form()
        context['comments'] = self.get_object().comments.all().order_by('-created_date')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Attach the current user and the post to the comment instance before saving
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = self.object
        comment.save()
        return super().form_valid(form)

# class CommentCreateView(CreateView):
#     model = Comment
#     template_name = 'blog/comment_form.html'
#     fields = ['content']

#     def form_valid(self, form):
#         # Attach the current user and the post to the comment instance before saving
#         form.instance.author = self.request.user
#         form.instance.post_id = self.kwargs['post_pk']
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('post-detail', kwargs={'pk': self.object.post.pk})
    

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'blog/comment_update_form.html'
    form_class = CommentForm
    context_object_name = 'comment'

    def get_success_url(self):
        # Redirect back to the post detail page after updating
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        # Ensure only the author of the comment can update it
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    context_object_name = 'comment'

    def get_success_url(self):
        # Redirect back to the post detail page after deleting
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        # Ensure only the author of the comment can delete it
        comment = self.get_object()
        return self.request.user == comment.author



    
