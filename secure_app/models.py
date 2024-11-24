from django.contrib.auth.models import AbstractUser
from django.db import models
from django_cryptography.fields import encrypt


class CustomUser(AbstractUser):
    phone_number = encrypt(models.CharField(max_length=15, blank=True))
    is_two_factor_enabled = models.BooleanField(default=False)


class SensitiveData(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sensitive_info = encrypt(models.TextField())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sensitive data for {self.user.username}"
