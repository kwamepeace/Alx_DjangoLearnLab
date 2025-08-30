

from django.urls import path
from .views import UserRegistrationView, LoginView, ProtectedView, LogoutView

urlpatterns = [
    # URL for user registration.
    path('register/', UserRegistrationView.as_view(), name='register'),
    # URL for user login and token retrieval.
    path('login/', LoginView.as_view(), name='login'),
    # URL for token-protected content.
    path('protected/', ProtectedView.as_view(), name='protected'),
    # URL to log out and delete a token.
    path('logout/', LogoutView.as_view(), name='logout'),
]

