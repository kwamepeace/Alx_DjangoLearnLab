from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User
from django.contrib.auth import get_user_model


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for handling user registration.
    It extends ModelSerializer to automatically handle saving a new User instance.
    """
    class Meta:
        model = User
        # The fields a user needs to provide for registration.
        fields = ['username', 'email', 'bio', 'profile_picture', 'password']
        # Set extra keyword arguments for password to ensure it is not readable.
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # This method is called by the view's create() method.
        # It creates a new user with a correctly hashed password.
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )

        
        # Create a token for the newly registered user.
        # This is optional, but useful for automatic login after registration.
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer to handle user login.
    It validates credentials and returns an authentication token.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        """
        Custom validation to authenticate the user.
        """
        username = data.get('username')
        password = data.get('password')

        if username and password:
            # The authenticate function checks the credentials against the database.
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    # Get or create a token for the authenticated user.
                    token, created = Token.objects.get_or_create(user=user)
                    data['token'] = token.key
                    return data
                else:
                    raise serializers.ValidationError("User account is inactive.")
            else:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
