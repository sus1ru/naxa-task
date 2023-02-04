""" Test for the interns API """

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """ Create dummy users and return """
    return get_user_model().objects.create_user(**params)


class GuestUserApiTests(TestCase):
    """ Test the guest feauters of the users API """
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """ Test of the user creation works """
        payload = {
            'email': 'lebowski@example.com',
            'password': 'peeonmyrug',
            'name': 'thedude',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Get the user object with the given email
        user = get_user_model().objects.get(email=payload['email'])
        # Check the password in present in the user object
        self.assertTrue(user.check_password(payload['password']))
        # Check if the password hash is returned while user creation
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """ Test whether a user with the email already exists """
        payload = {
            'email': 'lebowski@example.com',
            'password': 'peeonmyrug',
            'name': 'thedude',
        }
        """
        **payload splits the arguments as
        (email='lebowski@example.com', password='peeonmyrug'...)
        """
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """
        Test whether a password is less than
        6 characters and return error if true
        """
        payload = {
            'email': 'lebowski@example.com',
            'password': 'pp',
            'name': 'thedude',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
        Test creation of token for a user
        (using token based authentication)
        """
        user_details = {
            'email': 'lebowski@example.com',
            'password': 'peeontherug',
            'name': 'thedude',
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        create_user(
            email='thedriver@example.com',
            password='autism101',
        )
        payload = {
            'email': 'notadriver@example.com',
            'password': 'chaddening',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        payload = {
            'email': 'thedriver@example.com',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ Test authentication is required for users """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """ Test API requests accessible to authenticated users """

    def setUp(self):
        self.user = create_user(
            email='lebowski@example.com',
            password='peeontherug',
            name='thedude',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """ Test retrieving profile for authenticated users """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """
        Test POST is not allowed for the 'me' endpoint
        """
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        Test updating of the user profiles
        """
        payload = {
            'name': 'waltuh',
            'password': 'chaddening',
        }
        res = self.client.patch(ME_URL, payload)

        """ Manual invoke to refresh the data """
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
