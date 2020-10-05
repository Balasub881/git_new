from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.text import gettext_lazy as _


from .models import User, UploadImageTest


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, Please try again..!!')

        if not user.is_active:
            raise AuthenticationFailed('Account Disabled, Please contact Admin..!!')



        return {
            'password': user.password,
            'tokens': user.tokens(),
            'email': user.email
        }

        return super().validate(attrs)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImageTest
        fields = ('name', 'image')

