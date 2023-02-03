"""
Tests for the django admin modifications
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """ Tests for Django admin """
    def setUp(self):
        """ Create superuser and user for the tests """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="louiscypher@example.com",
            password="groundcontroltomajortom",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="ryangoose@example.com",
            password="idriveee",
            name="basedboi",
        )
    
    def test_user_list(self):
        """ Test for the users listed in the page """
        url = reverse("admin:core_user_changelist")                     # Reversing to get the url for user list from the django admin through
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """ Test editing of the user works """
        url = reverse("admin:core_user_change", args=[self.user.id])     # Get the url for user page from the id
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test the create user page works """
        url = reverse('admin:core_user_add')                            # Get the url of the page for user creation
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
