from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from market.models import CustomUser


class TestViews(TestCase):

    def test_register_producer_view(self):
        url = reverse('register_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        register_user = reverse('register_user')
        self.assertContains(response, f'href="{register_user}"')

        login_user = reverse('login_user')
        self.assertContains(response, f'href="{login_user}"')


class UserAuthenticationTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='testpassword123')

    def test_user_login(self):
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.get(reverse('home'))

        self.assertTrue(response.context['user'].is_authenticated)