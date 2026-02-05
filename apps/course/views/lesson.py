from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.authentication.perms.custom_perms import (
    IsCourseOwner,
    IsInstructor,
    IsLessonInstructorOwner,
    IsStudent,
)
from base.views.generic_views import (
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from ..models import Lesson
from ..serializers import (
    LessonCreateSerializer,
    LessonDetailSerializer,
    LessonListSerializer,
    LessonUpdateSerializer,
)


class LessonListView(CustomGenericListView):
    """
    List all lessons for a course.
    """

    serializer_class = LessonListSerializer
    permission_classes = [IsLessonInstructorOwner]

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return Lesson.objects.filter(course_id=course_id).order_by("order")


class LessonCreateView(CustomGenericCreateView):
    """
    Create a new lesson (Instructors only).
    """

    serializer_class = LessonCreateSerializer
    permission_classes = [IsInstructor]
    success_response_message = "Lesson created successfully."


class LessonRetrieveView(CustomGenericRetrieveView):
    """
    Retrieve lesson details.
    """

    serializer_class = LessonDetailSerializer
    queryset = Lesson.objects.all()


class LessonUpdateView(CustomGenericUpdateView):
    """
    Update a lesson (Instructor owner only).
    """

    serializer_class = LessonUpdateSerializer
    permission_classes = [IsInstructor, IsLessonInstructorOwner]

    def get_queryset(self):
        return Lesson.objects.filter(course__instructor=self.request.user)


class LessonDeleteView(generics.DestroyAPIView):
    """
    Delete a lesson (Instructor owner only).
    """

    permission_classes = [IsInstructor, IsLessonInstructorOwner]

    def get_queryset(self):
        return Lesson.objects.filter(course__instructor=self.request.user)
