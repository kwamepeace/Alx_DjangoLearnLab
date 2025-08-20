from django.urls import path
from django.contrib import admin
from .views import register, login_view, logout_view, home, posts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path ('register/', register ,name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('posts/', posts, name='posts'),

    ]


''' 
URLs definition
login = http://127.0.0.1:8000/blog/login/
register = http://127.0.0.1:8000/blog/register/
logout = http://127.0.0.1:8000/blog/logout/
'''
