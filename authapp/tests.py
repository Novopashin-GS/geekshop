from django.test import TestCase
from django.test.client import Client
from authapp.models import ShopUser
from django.core.management import call_command


class TestUserManagement(TestCase):
    def setUp(self):
        self.superuser = ShopUser.objects.create_superuser('django2', 'django2@geekshop.local', 'geekbrains1')

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'Мой магазин')
        self.assertNotContains(response, 'Пользователь', status_code=200)
        self.client.login(username='django2', password='geekbrains1')
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertContains(response, 'Пользователь', status_code=200)




