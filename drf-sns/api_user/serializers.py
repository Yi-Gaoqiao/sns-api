from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from core.models import Profile, FriendRequest

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
    
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        user = get_user_model().objects.create_user(**validated_data)

        return user

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the user profile"""

    class Meta:
        model = Profile
        fields = ('id', 'nickName', 'user', 'created_at', 'img')
        # extra_kwargs = {'user': {'read_only': True}}
        read_only_fields = ('user', 'created_at',)


class FriendRequestSerializer(serializers.ModelSerializer):
    """Serializer for friend request model"""

    class Meta:
        model = FriendRequest
        fields = ('id', 'askFrom', 'askTo', 'approved')
        extra_kwargs = {'askFrom': {'read_only': True}}