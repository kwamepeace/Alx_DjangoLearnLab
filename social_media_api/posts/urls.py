from rest_framework_nested import routers
from .views import PostViewSet, CommentViewSet

# Create a top-level router for the 'posts' endpoint
router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

# Create a nested router for 'comments' under 'posts'
posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

# The API URLs are now determined automatically by the routers
urlpatterns = router.urls + posts_router.urls
