from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.contrib.auth import authenticate, login
from .models import CustomUser as User
from .serializers import UserSerializer

class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.
    Uses the UserSerializer to create a new user instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    """
    API view for user login.
    Authenticates the user and returns an authentication token.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.pk, 'username': user.username}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProtectedView(APIView):
    """
    An example of a protected API endpoint.
    Only accessible by authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': f'Welcome, {request.user.username}! This is a protected endpoint.'})

class UserLogoutView(APIView):
    """
    API view to log a user out by deleting their token.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Could not log out. Token not found.'}, status=status.HTTP_400_BAD_REQUEST)
