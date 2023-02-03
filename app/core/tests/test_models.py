"""
Test for custom models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Model Test Class"""

    def test_create_user_with_email_successful(self):
        email = "pp@example.com"
        password = "mypphurt"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test whether email is normalized for new users. """
        sample_emails = [
            ["test1@EXAMPLE.COM", "test1@example.com"],
            ["Test2@Example.Com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.com", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'keysersoze')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """ Test whether creating a user without an email raises ValueError """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'keysersoze')

    def test_create_super_user(self):
        """ Test creation of a superuser """
        user = get_user_model().objects.create_superuser("keyser@example.com", 'keysersoze')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
