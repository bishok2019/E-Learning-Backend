from .course import (
    CourseCreateView,
    CourseListView,
    CourseRetrieveView,
    CourseUpdateView,
    # CourseDeleteView,
)
from .enrollment import (
    EnrollmentCreateView,
    EnrollmentListView,
    EnrollmentRetrieveView,
)
from .lesson import (
    LessonCreateView,
    LessonDeleteView,
    LessonListView,
    LessonRetrieveView,
    LessonUpdateView,
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
