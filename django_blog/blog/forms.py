from django.contrib.auth.forms import  UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Comment





class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user registration, extending the UserCreationForm.
    
    """
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    class Meta:
        model = User # To extend the default
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    Form for user login, extending the Form class.
    
    """
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if not username or not password:
            raise forms.ValidationError("Both fields are required.")
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']


class CommentForm(forms.ModelForm):
    """
    A form for creating and updating comments on a blog post.
    The form handles validation automatically for the content field.

    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder' : 'Write your comment here ....',
                'rows': 4
            })
        }