from ..serializers import (
    LessonCompletionCreateSerializer,
    LessonCompletionListSerializer,
)
from apps.authentication.custom_perms import IsStudent
from base.views.generic_views import (
    CustomGenericCreateView,
    CustomGenericListView,
)
from ..models import Progress

class LessonProgressCreateView(CustomGenericCreateView):
    """
    Mark a lesson as completed (Students only).
    """
    serializer_class = LessonCompletionCreateSerializer
    permission_classes = [IsStudent]


class LessonProgressListView(CustomGenericListView):
    """
    List all completed lessons for an enrollment.
    """
    serializer_class = LessonCompletionListSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        enrollment_id = self.kwargs.get("enrollment_id")
        return Progress.objects.filter(
            enrollment_id=enrollment_id,
            enrollment__student=self.request.user
        )