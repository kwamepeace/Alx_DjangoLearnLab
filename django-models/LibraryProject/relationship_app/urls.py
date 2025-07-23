from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views 

app_name = 'relationship_app' 

urlpatterns = [
    path('books/', views.list_books, name='book_list'),
    path('libraries/<int:pk>/', views.LibraryDetailView.get_library(), name='library_detail'),

    # --- Authentication URLs ---
    path('register/', views.register, name='register'),

    # User Login 
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # User Logout 
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html', next_page='relationship_app:login'), name='logout'),
]