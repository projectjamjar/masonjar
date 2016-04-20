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
            "email": "test@projectjamjar.com",
            "invite": "48c-926669e40c2196dd94de"
        }
        response = self.client.post(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Account.objects.count(), 1)
        # self.assertEqual(Account.objects.get().name, 'DabApps')