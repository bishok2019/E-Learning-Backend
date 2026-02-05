from django.contrib import admin

from .models import Course, Enrollment, Lesson, Progress

admin.site.register(
    [
        Course,
        Enrollment,
        Lesson,
        Progress,
    ]
)
