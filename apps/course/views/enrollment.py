from rest_framework import generics, permissions

from apps.authentication.models import UserTypeEnum
from apps.authentication.perms.custom_perms import IsStudent

from ..models import Enrollment
from ..serializers import (
    EnrollmentCreateSerializer,
    EnrollmentDetailSerializer,
    EnrollmentListSerializer,
)


class EnrollmentListView(generics.ListAPIView):
    """
    List all enrollments for the current student.
    """

    serializer_class = EnrollmentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserTypeEnum.STUDENT:
            return Enrollment.objects.filter(student=user)
        elif user.user_type == UserTypeEnum.INSTRUCTOR:
            # Instructors can see enrollments in their courses
            return Enrollment.objects.filter(course__instructor=user)
        return Enrollment.objects.none()


class EnrollmentCreateView(generics.CreateAPIView):
    """
    Enroll in a course (Students only).
    """

    serializer_class = EnrollmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]


class EnrollmentRetrieveView(generics.RetrieveAPIView):
    """
    Retrieve enrollment details with progress information.
    """

    serializer_class = EnrollmentDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserTypeEnum.STUDENT:
            return Enrollment.objects.filter(student=user)
        elif user.user_type == UserTypeEnum.INSTRUCTOR:
            return Enrollment.objects.filter(course__instructor=user)
        return Enrollment.objects.none()
