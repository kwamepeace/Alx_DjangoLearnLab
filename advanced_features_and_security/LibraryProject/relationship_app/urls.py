from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'relationship_app'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('books/', views.list_books, name='book_list'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='relationship_app:login'), name='logout'),

    # DASHBOARD VIEW REFERENCES:
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('librarian-dashboard/', views.librarian_dashboard, name='librarian_dashboard'),
    path('member-dashboard/', views.member_dashboard, name='member_dashboard'),

    path('books/add_book/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]