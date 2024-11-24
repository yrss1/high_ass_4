from django.db import models
from django.contrib.auth.models import User
from .encryption import encrypt_value, decrypt_value


class EncryptedCharField(models.CharField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return decrypt_value(value)

    def to_python(self, value):
        if value is None:
            return value
        return decrypt_value(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return encrypt_value(value)


class EncryptedTextField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return decrypt_value(value)

    def to_python(self, value):
        if value is None:
            return value
        return decrypt_value(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return encrypt_value(value)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = EncryptedCharField(max_length=256)  # Increased max_length to accommodate encrypted data
    address = EncryptedTextField()
    date_of_birth = models.DateField()
    is_premium = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.phone_number:
            self.phone_number = encrypt_value(self.phone_number)  # Шифруем номер телефона перед сохранением
        super().save(*args, **kwargs)
    def __str__(self):
        return self.user.username


class SecureData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    secret_key = EncryptedCharField(max_length=256)  # Increased max_length to accommodate encrypted data
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Email(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email to {self.recipient}: {self.subject}"
