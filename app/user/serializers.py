"""
Serializers for the user API view
"""

from django.contrib.auth import (
    get_user_model,
    authenticate
)

from rest_framework import serializers
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user model
    (Get the API result and create a custom model out of it)
    """
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def create(self, validated_data):
        """
        Create a new user and return with password encrypted
        (Override the create method for password encryption)
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Modify and return users details
        (Override the update method for password encryption)
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for the auth token of the user
    (Using token based authentication)
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('Invalid credentials, unable to authenticate!')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
