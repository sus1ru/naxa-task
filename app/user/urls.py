"""
URLs mapping for user API View
"""

from user import views

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('attendances', views.AttendanceViewSet)

app_name = 'user'

urlpatterns = [
    # as_view() converts the class based view into supported django view
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('', include(router.urls)),
]
