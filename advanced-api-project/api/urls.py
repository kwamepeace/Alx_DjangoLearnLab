from django.urls import path
from .views import ListView, DetailView, CreateView, UpdateView, DeleteView



urlpatterns = [
    path('books/', ListView.as_view(), name='book-list'),
    path('books/create/', CreateView.as_view(), name='book-create'),
    path('books/update/<str:title>/', UpdateView.as_view(), name='book-update'),
    path('books/delete/<int:pk>/', DeleteView.as_view(), name='book-delete'),
    path('book/<int:pk>/', DetailView.as_view(), name='book-detail'),
]
