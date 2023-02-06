"""
Class based views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    AttendanceSerializer,
    AttendanceDetailSerializer
)

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Attendance


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system
    (CreateAPIView handles http post request for creating objects)
    """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    Create a new auth token for the user
    (Override ObtainAuthToken to use email as username)
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenicated user
    (RetrieveUpdateAPIView allows to retrieve and update objects)
    """
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve and return the authenticated user
        (Override: custom method to deal with get requests)
        """
        return self.request.user


class AttendanceViewSet(viewsets.ModelViewSet):
    """View to manage Attendance APIs."""
    serializer_class = AttendanceDetailSerializer
    queryset = Attendance.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve atendance for authenticated users."""
        return self.queryset.filter(
            user=self.request.user
        ).order_by('-attended_at')

    def get_serializer_class(self):
        """Return the serializer for requests."""
        if self.action == 'list' or self.action == 'create':
            return AttendanceSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Attendance."""
        serializer.save(user=self.request.user)
