from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jamjar.users.models import User
from django.db import transaction, IntegrityError

class SignupTests(APITestCase):
    def setUpUser(self):
        try:
            # Duplicates should be prevented.
            with transaction.atomic():
                # Create a user with the username "test"
                User.objects.create(username='test',
                                    email='test@projectjamjar.com',
                                    first_name='Test',
                                    last_name='User1')
        except IntegrityError:
            pass

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

    def test_signup_duplicate_username_failure(self):
        """
        Ensure we cannot sign up with an existing username
        """
        self.setUpUser()

        url = reverse('signup')
        data = {
            "username": "test",
            "first_name": "Test",
            "last_name": "User2",
            "password": "password",
            "confirm": "password",
            "email": "test@projectjamjar.com"
        }
        response = self.client.post(url, data, format='json')

        # Check the status code
        self.assertEqual(response.status_code, 422)

        # Make sure we still only have 1 user (the original one) in the DB
        self.assertEqual(User.objects.count(), 1)
