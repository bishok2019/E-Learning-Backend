from django.urls import include, path

from .views import (
    CourseCreateView,
    CourseListView,
    CourseRetrieveView,
    CourseUpdateView,
    EnrollmentCreateView,
    EnrollmentListView,
    EnrollmentRetrieveView,
    LessonCreateView,
    LessonDeleteView,
    # CourseDeleteView,
    LessonListView,
    LessonProgressCreateView,
    LessonProgressListView,
    LessonRetrieveView,
    LessonUpdateView,
)

course_patterns = [
    path("list", CourseListView.as_view(), name="course-list"),
    path("create", CourseCreateView.as_view(), name="course-create"),
    path("retrieve/<int:pk>", CourseRetrieveView.as_view(), name="course-retrieve"),
    path("update/<int:pk>", CourseUpdateView.as_view(), name="course-update"),
    # path("delete/<int:pk>", CourseDeleteView.as_view(), name="course-delete"),
]

lesson_patterns = [
    path("list", LessonListView.as_view(), name="lesson-list"),
    path("create", LessonCreateView.as_view(), name="lesson-create"),
    path("retrieve/<int:pk>", LessonRetrieveView.as_view(), name="lesson-retrieve"),
    path("update/<int:pk>", LessonUpdateView.as_view(), name="lesson-update"),
    path("delete/<int:pk>", LessonDeleteView.as_view(), name="lesson-delete"),
]

enrollment_patterns = [
    path("list", EnrollmentListView.as_view(), name="enrollment-list"),
    path("create", EnrollmentCreateView.as_view(), name="enrollment-create"),
    path(
        "retrieve/<int:pk>",
        EnrollmentRetrieveView.as_view(),
        name="enrollment-retrieve",
    ),
]

progress_patterns = [
    path(
        "<int:enrollment_id>/completions/create",
        LessonProgressCreateView.as_view(),
        name="lesson-progress-create",
    ),
    path(
        "<int:enrollment_id>/completions/list",
        LessonProgressListView.as_view(),
        name="lesson-progress-list",
    ),
]

urlpatterns = [
    path("courses/", include(course_patterns)),
    path("lessons/", include(lesson_patterns)),
    path("enrollments/", include(enrollment_patterns)),
    path("progress/", include(progress_patterns)),
]
