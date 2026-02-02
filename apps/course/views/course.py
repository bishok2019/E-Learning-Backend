from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from apps.authentication.custom_perms import IsInstructor, IsInstructorOwner
from apps.authentication.models import UserTypeEnum
from base.views.generic_views import (
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from ..models import Course, CourseStatusEnum
from ..serializers import (
    CourseCreateSerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    CourseUpdateSerializer,
)


class CourseListView(CustomGenericListView):
    """
    List all published courses for students.
    Instructors see all their own courses.
    """

    serializer_class = CourseListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserTypeEnum.INSTRUCTOR:
            # Instructors see their own courses
            return Course.objects.filter(instructor=user)
        else:
            # Students see only published courses
            return Course.objects.filter(status=CourseStatusEnum.PUBLISHED)


class CourseCreateView(CustomGenericCreateView):
    """
    Create a new course (Instructors only).
    """

    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated, IsInstructor]


class CourseRetrieveView(CustomGenericRetrieveView):
    """
    Retrieve course details.
    """

    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserTypeEnum.INSTRUCTOR:
            return Course.objects.filter(instructor=user)
        else:
            return Course.objects.filter(status=CourseStatusEnum.PUBLISHED)


class CourseUpdateView(CustomGenericUpdateView):
    """
    Update a course (Instructor owner only).
    """

    serializer_class = CourseUpdateSerializer
    permission_classes = [IsAuthenticated, IsInstructor, IsInstructorOwner]

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)


# class CourseDeleteView(CustomGenericUpdateView):
#     """
#     Delete a course (Instructor owner only).
#     """
#     permission_classes = [permissions.IsAuthenticated, IsInstructor, IsInstructorOwner]

#     def get_queryset(self):
#         return Course.objects.filter(instructor=self.request.user)
