from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jamjar.users.models import User

class AccountTests(APITestCase):
    def test_signup_success(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('signup')
        data = {
            "username": "test",
            "first_name": "Test",
            "last_name": "User",
            "password": "password",
            "confirm": "password",
            "email": "test@projectjamjar.com"
        }
        response = self.client.post(url, data, format='json')

        # We should really change this endpoint to return 201
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.get()
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.email, 'test@projectjamjar.com')
