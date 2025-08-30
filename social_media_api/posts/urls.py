from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentListCreateView, CommentDetailView

urlpatterns = [
    # URLs for Posts
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # URLs for Comments (nested under posts)
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
