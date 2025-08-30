from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment


class PostListCreateView(generics.ListCreateAPIView):
    """
    API view to list all posts or create a new post.
    GET: List all posts.
    POST: Create a new post.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        # Return all posts ordered by creation date (newest first)
        return Post.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        # Set the author of the post to the current user
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific post by ID.
    GET: Retrieve a post.
    PUT: Update a post.
    DELETE: Delete a post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'


class CommentListCreateView(generics.ListCreateAPIView):
    """
    API view to list all comments for a specific post or create a new comment.
    GET: List all comments for a post.
    POST: Create a new comment for a post.
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        # Filter comments by the post ID provided in the URL
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post__id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        # Set the author of the comment to the current user and associate it with the post
        post_id = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post_id)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific comment by ID.
    GET: Retrieve a comment.
    PUT: Update a comment.
    DELETE: Delete a comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'


