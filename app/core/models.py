"""
User Database Models.
"""
from datetime import datetime as date

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create a new user and assign the roles, save them, then return"""
        if not email:
            raise ValueError('Please enter a valid email...')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, password):
        """Create a staff and assign the roles, save them, then return"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create a superuser and assign the roles, save them, then return"""
        user = self.create_staff(email, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Task(models.Model):
    """Model for task object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="creator",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assignee_intern = models.EmailField(max_length=255)
    assignee_intern_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="executor",
        on_delete=models.CASCADE,
        null=True,
    )

    completion = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class User(AbstractBaseUser, PermissionsMixin):
    """Users in the Organization"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


# class AsignTask(models.Model):
#     items = models.ManyToManyField(Task, through='PackItem')


# class TaskList(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     pack = models.ForeignKey(AsignTask, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)


class Attendance(models.Model):
    """Attendance for the users."""
    date = models.CharField(
        max_length=16,
        default=date.today().strftime("%Y-%m-%d"),
        blank=False,
    )
    attended_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    attendance_last_modified = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("date", "user")

    PRESENT = 'present'
    ABSENT = 'absent'
    ATTENDANCE_STATUS = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
    ]

    status = models.CharField(
        max_length=8,
        choices=ATTENDANCE_STATUS,
        default=ABSENT
    )

    def __str__(self):
        return f"{self.user.name}: {self.status.title()}"
