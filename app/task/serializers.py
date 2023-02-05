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


class TaskDetailSerializer(TaskSerializer):
    """Serializer for the task detail view.."""
    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['description']
