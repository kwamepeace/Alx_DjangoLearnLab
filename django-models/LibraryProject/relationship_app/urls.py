from django.urls import path
from django.contrib.auth import views as auth_views 
from .views import book_list_view, LibraryDetailView, register

app_name = 'relationship_app' 

urlpatterns = [
    path('books/', book_list_view, name='book_list'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='relationship_app/login.html',
        redirect_authenticated_user=True 
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        template_name='relationship_app/logout.html',
        next_page='relationship_app:login' 
    ), name='logout'),
]