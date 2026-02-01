from .course import (
    CourseListView,
    CourseCreateView,
    CourseRetrieveView,
    CourseUpdateView,
    # CourseDeleteView,
)
from .lesson import (
    LessonListView,
    LessonCreateView,
    LessonRetrieveView,
    LessonUpdateView,
    LessonDeleteView,
)
from .enrollment import (
    EnrollmentListView,
    EnrollmentCreateView,
    EnrollmentRetrieveView,
)
from .progress import (
    LessonProgressCreateView,
    LessonProgressListView,
)

__all__ = [
    "CourseListView",
    "CourseCreateView",
    "CourseRetrieveView",
    "CourseUpdateView",
    "CourseDeleteView",
    "LessonListView",
    "LessonCreateView",
    "LessonRetrieveView",
    "LessonUpdateView",
    "LessonDeleteView",
    "EnrollmentListView",
    "EnrollmentCreateView",
    "EnrollmentRetrieveView",
    "LessonProgressCreateView",
    "LessonProgressListView",
]