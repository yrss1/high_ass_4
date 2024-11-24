from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, SecureData, Email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'date_of_birth', 'is_premium']


class SecureDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecureData
        fields = ['id', 'title', 'description', 'secret_key', 'url', 'created_at', 'updated_at']
        extra_kwargs = {'secret_key': {'write_only': True}}


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['id', 'recipient', 'subject', 'body', 'sent', 'created_at']
