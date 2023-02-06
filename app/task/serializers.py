"""
Serializers for Task APIs.
"""
from rest_framework import serializers
from core.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the tasks."""
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'assignee_intern',
            'completion',
        ]
        read_only_fields = ['id']
    
    # def create(self, validated_data):
    #     """
    #     Create and assign user field based on the user email passed.
    #     """
    #     user_email = validated_data.get("assignee_intern")
    #     user = get_user_model().objects.get(email__exact='user')
    #     return super().create(validated_data)


class TaskDetailSerializer(TaskSerializer):
    """Serializer for the task detail view."""
    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['description']

# class AttendanceSerializer(serializers.ModelSerializer):
#     """Serializer for Attendance"""
#     class Meta:
#         model = Attendance
#         fields = ['id', 'status']
#         read_only_fields = ['id']


# class AttendanceDetailSerializer(AttendanceSerializer):
#     """Serializer for Attendance"""
#     class Meta(AttendanceSerializer.Meta):
#         fields = AttendanceSerializer.Meta.fields + ['date']
