from django.urls import path
from django.contrib.auth import views as auth_views 
# or from django.contrib.auth.views import LoginView, LogoutView
from .views import views
from .views import list_books

app_name = 'relationship_app' 

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('books/', views.list_books, name='book_list'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'), 
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html', next_page='relationship_app:login'), name='logout'),
    path('admin-dashboard/', views.admin_view, name='admin_dashboard'), 
    path('librarian-dashboard/', views.librarian_view, name='librarian_dashboard'), 
    path('member-dashboard/', views.member_view, name='member_dashboard'),
    path('books/add_book/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]