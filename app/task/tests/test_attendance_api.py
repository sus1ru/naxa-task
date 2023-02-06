"""Tests for attendance API endpoint."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Attendance
from task.serializers import (
    AttendanceSerializer,
)

ATTENDANCE_URL = reverse('task:attendance-list')

def create_user(email = "pp@example.com", password = "mypphurt"):
    """Create and return a dummy user."""
    return get_user_model().objects.create_user(email, password)

def detail_url(attendance_id):
    """Create and return a attendance detail URL."""
    return reverse('task:attendance-detail', args=[attendance_id])


class PublicAttendanceApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required for Attendance API."""
        res = self.client.get(ATTENDANCE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTaskApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)
    
    def test_attendance_duplication(self):
        """Test whether creation of more than one attendance in a day causes error."""
        Attendance.objects.create(user=self.user, status=Attendance.ABSENT)
        with self.assertRaises(IntegrityError):
            Attendance.objects.create(user=self.user, status=Attendance.PRESENT)

    def test_retrieve_todays_attendance(self):
        """Test retrieving of the attendance list."""
        Attendance.objects.create(user=self.user, status=Attendance.ABSENT)

        res = self.client.get(ATTENDANCE_URL)

        attendance = Attendance.objects.all().order_by('-id')
        serializer = AttendanceSerializer(attendance, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_attendance_not_visible_to_interns(self):
        """Test the attendance of an intern is visible to themselves only."""
        user2 = create_user(email='pp2@example.com')
        Attendance.objects.create(user=user2, status=Attendance.ABSENT)
        attendance = Attendance.objects.create(user=self.user, status=Attendance.PRESENT)
        res = self.client.get(ATTENDANCE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['status'], attendance.status)
        self.assertEqual(res.data[0]['id'], attendance.id)

    def test_update_attendance(self):
        """Test updating an attendance."""
        attendance = Attendance.objects.create(user=self.user, status=Attendance.ABSENT)

        payload = {'status': attendance.PRESENT}
        url = detail_url(attendance.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        attendance.refresh_from_db()
        self.assertEqual(attendance.status, payload['status'])

    def test_delete_attendance(self):
        """Test deleting an attendance."""
        attendance = Attendance.objects.create(user=self.user, status=Attendance.ABSENT)

        url = detail_url(attendance.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Attendance.objects.filter(user=self.user)
        self.assertFalse(tags.exists())

    def test_create_attendance(self):
        """Test creation of attendance."""
        payload = {'status': Attendance.PRESENT}

        res = self.client.post(ATTENDANCE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        attendance = Attendance.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(attendance, k), v)
        self.assertEqual(attendance.user, self.user)
