from django.db import models

from base.models import AbstractBaseModel


class Enrollment(AbstractBaseModel):
    student = models.ForeignKey(
        "authentication.CustomUser",
        on_delete=models.CASCADE,
        related_name="enrollments",
        help_text="Student enrolled in the course.",
    )
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="enrollments",
        help_text="Course the student is enrolled in.",
    )
    is_completed = models.BooleanField(
        default=False, help_text="Whether the student has completed the course."
    )
    completed_at = models.DateTimeField(
        null=True, blank=True, help_text="Timestamp when the course was completed."
    )

    class Meta:
        db_table = "enrollments"
        unique_together = ["student", "course"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student.full_name} - {self.course.title}"

    @property
    def total_lessons(self):
        return self.course.total_lessons

    @property
    def completed_lessons_count(self):
        return self.completed_lessons.count()

    @property
    def completion_percentage(self):
        total = self.total_lessons
        if total == 0:
            return 0
        return round((self.completed_lessons_count / total) * 100, 2)
