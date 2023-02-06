"""
Views for the task API.
"""
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action

from core.models import Task
from task import serializers


class TaskViewSet(viewsets.ModelViewSet):
    """View to manage task APIs."""
    serializer_class = serializers.TaskDetailSerializer
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def get_queryset(self):
        """Retrieve task for authenticated users."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

        # if self.request.GET.get('assignee_intern'):
        #     self.queryset = self.queryset.filter(assignee_intern=self.request.GET.get('assignee_intern')).order_by('-id')
        #     return self.queryset
        # else:
        #     raise ValueError

    def get_serializer_class(self):
        """Return the serializer for requests."""
        if self.action == 'list':
            return serializers.TaskSerializer

        return self.serializer_class
    
    def get_serializer(self, *args, **kwargs):
        # leave this intact
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()

        """
        Intercept the request and see if it needs tweaking
        """
        user_email = self.request.data.get("assignee_intern")
        user = get_user_model().objects.filter(email__exact=user_email)
        if user:
            # Copy and manipulate the request
            draft_request_data = self.request.data.copy()
            draft_request_data["assignee_intern_user"] = user
            kwargs["data"] = draft_request_data
            return serializer_class(*args, **kwargs)
        """
        If not mind your own business and move on
        """
        return serializer_class(*args, **kwargs)
    
    def perform_create(self, serializer):
        """Create a new Attendance."""
        serializer.save(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     """Create a new Task."""
    #     user_email = kwargs['assignee_intern']
    #     user = get_user_model().objects.get(email__exact=user_email)
        
    #     # if request.user.id == request.data['author']:
    #     if user:
    #         kwargs['assignee_intern_user'] = user

    #         serializer = self.get_serializer(data=kwargs)
    #         serializer.is_valid(raise_exception=True)

    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     else:
    #         return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)


# class AttendanceViewSet(viewsets.ModelViewSet):
#     """View to manage Attendance APIs."""
#     serializer_class = serializers.AttendanceSerializer
#     queryset = Attendance.objects.all()
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         """Retrieve atendance for authenticated users."""
#         return self.queryset.filter(
#             user=self.request.user
#         ).order_by('-attended_at')

#     def get_serializer_class(self):
#         """Return the serializer for requests."""
#         if self.action != 'list':
#             return serializers.AttendanceDetailSerializer

#         return self.serializer_class

#     def perform_create(self, serializer):
#         """Create a new Attendance."""
#         serializer.save(user=self.request.user)
