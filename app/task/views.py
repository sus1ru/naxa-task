"""
Views for the task API.
"""

from rest_framework import (
    viewsets,
    mixins
) 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Task,
    Attendance
)
from task import serializers


class TaskViewSet(viewsets.ModelViewSet):
    """View to manage task APIs."""
    serializer_class = serializers.TaskDetailSerializer
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve task for authenticated users."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer for requests."""
        if self.action == 'list':
            return serializers.TaskSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Task."""
        serializer.save(user=self.request.user)


# class AttendanceViewSet(viewsets.ModelViewSet):
#     """View to manage Attendance APIs."""
#     serializer_class = serializers.AttendanceSerializer
#     queryset = Attendance.objects.all()
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         """Retrieve atendance for authenticated users."""
#         return self.queryset.filter(user=self.request.user).order_by('-attended_at')
    
#     def get_serializer_class(self):
#         """Return the serializer for requests."""
#         if self.action is not 'list':
#             return serializers.AttendanceDetailSerializer

#         return self.serializer_class

#     def perform_create(self, serializer):
#         """Create a new Attendance."""
#         serializer.save(user=self.request.user)
