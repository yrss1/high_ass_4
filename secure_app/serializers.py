from rest_framework import serializers
from .models import CustomUser, SensitiveData


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'is_two_factor_enabled']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class SensitiveDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensitiveData
        fields = ['id', 'sensitive_info', 'created_at', 'updated_at']


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
