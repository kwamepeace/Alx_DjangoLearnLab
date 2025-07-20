from django.contrib import admin
from django.urls import path, include 
from django.contrib.auth import views as auth_views
from .views import list_books, LibraryDetailView,  register_view, CustomLoginView, CustomLogoutView

app_name = 'relationship_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('relations/', include('relationship_app.urls', namespace='relationship_app')),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]