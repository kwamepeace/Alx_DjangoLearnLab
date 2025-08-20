from django.contrib.auth.forms import ModelForm
from django.contrib.auth.models import User


class UserLoginForm(ModelForm):
    """
    Form for user login, extending the ModelForm.
    
    """
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']
        

class UserLogoutForm(ModelForm):
    """
    Form for user logout, extending the ModelForm.
    
    """
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user