"""
Test for custom models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email = "pp@example.com", password = "mypphurt"):
    """Create and return a dummy user."""
    return get_user_model().objects.create_user(email, password)


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
        user = get_user_model().objects.create_superuser(
            "keyser@example.com",
            'keysersoze'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_task(self):
        """Test creation of a task"""
        users = {
            'staff': {
                'email': 'keyser@example.com',
                'password': 'keysersoze'
            },
            'assignee_intern': {
                'email': 'megamind@example.com',
                'password': 'roxanne'
            },
        }
        staff = get_user_model().objects.create_staff(**users['staff'])
        self.assertTrue(staff.is_staff)

        assignee_intern = get_user_model().objects.create_user(
            **users['assignee_intern']
        )
        self.assertEqual(
            assignee_intern.email,
            users['assignee_intern']['email']
        )
        self.assertTrue(
            assignee_intern.check_password(
                users['assignee_intern']['password']
            )
        )

        task = {
            'user': staff,
            'title': 'Restart the Router',
            'assignee_intern': users['assignee_intern']['email'],
            'description': "Restart the router every 5 minutes.",
            'completion': False,
        }

        res = get_user_model().objects.get(email=task['assignee_intern'])
        self.assertEqual(res.email, task['assignee_intern'])

        task = models.Task.objects.create(**task)
        self.assertEqual(str(task), task.title)

    def test_create_attendance(self):
        """Test creation of attendance is successful."""
        user = create_user()
        attendance = models.Attendance.objects.create(user=user, status='P')

        self.assertEqual(str(attendance), attendance.status)
