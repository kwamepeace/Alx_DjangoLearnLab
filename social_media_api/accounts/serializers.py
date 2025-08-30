from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    Used for creating a new user during registration.
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'followers': {'read_only': True}, # The followers field should not be writeable by the user
            'profile_picture': {'required': False}, # Make profile picture optional
        }

    def create(self, validated_data):
        """
        Overrides the create method to correctly hash the user's password.
        """
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create(**validated_data)
        if password is not None:
            user.set_password(password)
            user.save()
        return user
