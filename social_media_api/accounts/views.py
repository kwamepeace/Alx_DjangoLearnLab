from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserRegistrationSerializer, LoginSerializer

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.
    Handles POST requests to create a new User instance.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class LoginView(APIView):
    """
    API view for user login.
    Takes username and password, returns an authentication token.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    """
    A protected API view that requires a valid token to access.
    Returns a success message to a logged-in user.
    """
    # This ensures that only users with a valid token can access this view.
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user will be the User instance authenticated by the token.
        return Response({
            "message": f"Welcome, {request.user.username}! You are authenticated."
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    API view for user logout.
    Deletes the user's authentication token.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # The token is available on the request.auth object.
        # We delete the token to log the user out.
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
