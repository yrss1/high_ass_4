from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import SecureData, UserProfile
from .encryption import encrypt_value, decrypt_value


class SecureDataAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_secure_data(self):
        data = {
            'title': 'Test Data',
            'description': 'This is a test',
            'secret_key': 'secret123',
            'url': 'https://example.com'
        }
        response = self.client.post('/api/secure-data/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SecureData.objects.count(), 1)
        self.assertEqual(SecureData.objects.get().title, 'Test Data')

    def test_get_secure_data(self):
        SecureData.objects.create(user=self.user, title='Test Data', description='This is a test',
                                  secret_key='secret123', url='https://example.com')
        response = self.client.get('/api/secure-data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Data')

    def test_update_secure_data(self):
        secure_data = SecureData.objects.create(user=self.user, title='Test Data', description='This is a test',
                                                secret_key='secret123', url='https://example.com')
        data = {'title': 'Updated Test Data'}
        response = self.client.patch(f'/api/secure-data/{secure_data.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SecureData.objects.get().title, 'Updated Test Data')

    def test_delete_secure_data(self):
        secure_data = SecureData.objects.create(user=self.user, title='Test Data', description='This is a test',
                                                secret_key='secret123', url='https://example.com')
        response = self.client.delete(f'/api/secure-data/{secure_data.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SecureData.objects.count(), 0)

    def test_encryption(self):
        # Test encryption and decryption
        original_value = "sensitive_data"
        encrypted_value = encrypt_value(original_value)
        decrypted_value = decrypt_value(encrypted_value)
        self.assertNotEqual(original_value, encrypted_value)
        self.assertEqual(original_value, decrypted_value)

        # Test that the encrypted value is actually stored in the database
        profile = UserProfile.objects.create(
            user=self.user,
            phone_number="1234567890",  # Эта строка будет зашифрована при сохранении
            address="123 Test St",
            date_of_birth="1990-01-01"
        )

        # Извлекаем значение из базы данных
        db_value = UserProfile.objects.filter(id=profile.id).values('phone_number').first()['phone_number']

        # Проверяем, что зашифрованное значение не совпадает с исходным номером телефона
        self.assertNotEqual(db_value, "1234567890")

        # Проверяем, что расшифрованное значение из базы данных соответствует исходному
        self.assertEqual(decrypt_value(db_value), "1234567890")

