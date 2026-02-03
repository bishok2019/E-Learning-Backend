from .course import (
    CourseCreateSerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    CourseUpdateSerializer,
)
from .enrollment import (
    EnrollmentCreateSerializer,
    EnrollmentDetailSerializer,
    EnrollmentListSerializer,
)
from .lesson import (
    LessonCreateSerializer,
    LessonDetailSerializer,
    LessonListSerializer,
    LessonUpdateSerializer,
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
