from django.urls import path
from .views import UserRegistrationView, LoginView, ProtectedView, UserLogoutView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
