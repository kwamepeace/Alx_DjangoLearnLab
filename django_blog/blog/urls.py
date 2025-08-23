from django.urls import path
from django.contrib import admin
from .views import (
    register, login_view, logout_view, home, 
    edit_profile, BlogsView, BlogCreateView, 
    BlogDetailView, BlogUpdateView, BlogDeleteView, 
    CommentUpdateView, CommentDeleteView, post_list_by_tag,
    search_results 
)
from django.conf import settings
from django.conf.urls.static import static

# Note: The `admin.site.urls` should typically be in your project's main urls.py file.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), 
    path('posts/', BlogsView.as_view(), name='posts'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post-detail'),
    path('post/new/', BlogCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', BlogUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='post-delete'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', edit_profile, name='edit_profile'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('tags/<slug:tag_slug>/', post_list_by_tag, name='posts_by_tag'),
    path('search/', search_results, name='search_results'),
    path('', PostByTagListView.as_view(), name='posts_by_tag'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

''' 
URLs definition
login = http://127.0.0.1:8000/blog/login/
register = http://127.0.0.1:8000/blog/register/
logout = http://127.0.0.1:8000/blog/logout/
create_new = http://127.0.0.1:8000/blog/post/new/


'''
