from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book_all')


urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), # Optional: For browsable API login/logout
    path('api/token/', obtain_auth_token, name='obtain_token'), # Endpoint to get token

]
