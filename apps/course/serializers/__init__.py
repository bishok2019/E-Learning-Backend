from .course import (
    CourseListSerializer,
    CourseCreateSerializer,
    CourseUpdateSerializer,
    CourseDetailSerializer,
)
from .lesson import (
    LessonListSerializer,
    LessonCreateSerializer,
    LessonUpdateSerializer,
    LessonDetailSerializer,
)
from .enrollment import (
    EnrollmentListSerializer,
    EnrollmentCreateSerializer,
    EnrollmentDetailSerializer,
)
from .progress import (
    LessonCompletionCreateSerializer,
    LessonCompletionListSerializer,
)

__all__ = [
    "CourseListSerializer",
    "CourseCreateSerializer",
    "CourseUpdateSerializer",
    "CourseDetailSerializer",
    "LessonListSerializer",
    "LessonCreateSerializer",
    "LessonUpdateSerializer",
    "LessonDetailSerializer",
    "EnrollmentListSerializer",
    "EnrollmentCreateSerializer",
    "EnrollmentDetailSerializer",
    "LessonCompletionCreateSerializer",
    "LessonCompletionListSerializer",
]