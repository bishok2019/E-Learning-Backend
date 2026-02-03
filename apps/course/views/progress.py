from apps.authentication.perms.custom_perms import IsStudent
from base.views.generic_views import (
    CustomGenericCreateView,
    CustomGenericListView,
)

from ..models import Enrollment, Progress
from ..serializers import (
    LessonCompletionCreateSerializer,
    LessonCompletionListSerializer,
)


class LessonProgressCreateView(CustomGenericCreateView):
    """
    Mark a lesson as completed (Students only).
    """

    serializer_class = LessonCompletionCreateSerializer
    permission_classes = [IsStudent]

    def get_serializer_context(self):
        """Add enrollment_id from URL to context"""
        context = super().get_serializer_context()
        enrollment_id = self.kwargs.get("enrollment_id")
        if enrollment_id:
            try:
                enrollment = Enrollment.objects.get(
                    id=enrollment_id, student=self.request.user
                )
                context["enrollment"] = enrollment
            except Enrollment.DoesNotExist:
                pass
        return context


class LessonProgressListView(CustomGenericListView):
    """
    List all completed lessons for an enrollment.
    """

    serializer_class = LessonCompletionListSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        enrollment_id = self.kwargs.get("enrollment_id")
        return Progress.objects.filter(
            enrollment_id=enrollment_id, enrollment__student=self.request.user
        )
