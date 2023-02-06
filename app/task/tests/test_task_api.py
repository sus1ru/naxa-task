"""Tests for task API endpoint."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Task
from task.serializers import (
    TaskSerializer,
    TaskDetailSerializer,
)


TASKS_URL = reverse('task:task-list')


def detail_url(task_id):
    """Create and return a task detail URL."""
    return reverse('task:task-detail', args=[task_id])


def create_task(user, **params):
    """Create and return a task"""
    defaults = {
        'title': 'Restart the Router',
        'assignee_intern': 'kanye@example.com',
        'description': 'Restart the router every 5 minutes.',
        'completion': False,
    }
    defaults.update(params)

    task = Task.objects.create(user=user, **defaults)
    return task


def create_user(email='kanye@example.com', password='followgod'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)

def create_superuser(email='kanye@example.com', password='followgod'):
    """Create and return a new user."""
    return get_user_model().objects.create_superuser(email, password)


class PublicTaskApiTests(TestCase):
    """Test unauthenticated public API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required for task API"""
        res = self.client.get(TASKS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTaskApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        superuser = {
            'email': 'mainman@exmple.com',
            'password': 'live@11B'
        }
        self.user = create_superuser(**superuser)
        self.client.force_authenticate(self.user)

    def test_retrieve_tasks_to_admin_only(self):
        """Test retrieving of the task list."""
        superuser = create_superuser()
        normal_user = create_user(email='humpty@example.com')

        create_task(user=self.user)
        create_task(user=self.user, assignee_intern='humpty@example.com', title='I cant take it anymore')
        create_task(user=self.user, title='Its all so tiresome')

        res = self.client.get(TASKS_URL)
        tasks = Task.objects.all().order_by('-id')
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_task_list_limited_to_user(self):
        """Test list of task is limited to authenticated users only."""
        other_user = create_user(
            email='humpty@example.com',
            password='drivershigh'
        )
        create_task(user=other_user)
        create_task(user=self.user)

        res = self.client.get(TASKS_URL)

        tasks = Task.objects.filter(user=self.user)
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_task_detail(self):
        """Test get task detail."""
        task = create_task(user=self.user)

        url = detail_url(task.id)
        res = self.client.get(url)

        serializer = TaskDetailSerializer(task)
        self.assertEqual(res.data, serializer.data)

    def test_create_task_admin_only(self):
        """Test creation of task."""
        superuser = create_superuser(
            email='humpty@example.com',
            password='drivershigh'
        )
        normaluser = create_user()

        payload = {
            'title': 'Hello! darkness',
            'assignee_intern': "humpty@example.com",
            'completion': False,
        }
        res = self.client.post(TASKS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        task = Task.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(task, k), v)
        self.assertEqual(task.user, self.user)

    # def test_partial_update(self):
    #     """Test partial update of a task."""

    #     task = create_task(
    #         user=self.user,
    #         title='Hello! darkness',
    #         assignee_intern='thedude@example.com',
    #         completion=False,
    #     )
    #     payload = {
    #         'title': 'Hello! pain',
    #         'assignee_intern': "thedude@example.com",
    #         'completion': False,
    #     }
    #     url = detail_url(task.id)
    #     res = self.client.patch(url, payload)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     task.refresh_from_db()
    #     self.assertEqual(task.title, payload['title'])
    #     self.assertEqual(task.user, self.user)
    #     self.assertEqual(task.completion, payload['completion'])
    #     self.assertEqual(task.assignee_intern, payload['assignee_intern'])

    # def test_full_update(self):
    #     """Test complete update of a task."""

    #     task = create_task(
    #         user=self.user,
    #         title='Hello! darkness',
    #         assignee_intern='thedude@example.com',
    #         completion=False,
    #     )
    #     payload = {
    #         'title': 'Hello! pain',
    #         'assignee_intern': 'mario@example.com',
    #         'description': 'Manifest the inner pain po.',
    #         'completion': False,
    #     }
    #     url = detail_url(task.id)
    #     res = self.client.put(url, payload)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     task.refresh_from_db()
    #     for k, v in payload.items():
    #         self.assertEqual(getattr(task, k), v)
    #     self.assertEqual(task.user, self.user)

    # def test_update_user_returns_error(self):
    #     """Test changing the task user results in an error."""
    #     new_user = create_user(
    #         email='mario@example.com',
    #         password='drivershigh'
    #     )
    #     task = create_task(user=self.user)

    #     payload = {'user': new_user.id}
    #     url = detail_url(task.id)
    #     self.client.patch(url, payload)

    #     task.refresh_from_db()
    #     self.assertEqual(task.user, self.user)

    # def test_delete_task(self):
    #     """Test deleting a task successful."""
    #     task = create_task(user=self.user)
    #     url = detail_url(task.id)
    #     res = self.client.delete(url)

    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Task.objects.filter(id=task.id).exists())

    # def test_delete_other_users_task_error(self):
    #     """Test deleting user users task results in an error."""
    #     new_user = create_user(
    #         email='humpty@example.com',
    #         password='drivershigh'
    #     )
    #     task = create_task(user=new_user)

    #     url = detail_url(task.id)
    #     res = self.client.delete(url)

    #     self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertTrue(Task.objects.filter(id=task.id).exists())
