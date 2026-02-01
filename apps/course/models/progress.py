from django.db import models
from base.models import AbstractBaseModel


class Progress(AbstractBaseModel):
    enrollment = models.ForeignKey(
        "course.Enrollment",
        on_delete=models.CASCADE,
        related_name="completed_lessons",
        help_text="Enrollment this progress belongs to."
    )
    lesson = models.ForeignKey(
        "course.Lesson",
        on_delete=models.CASCADE,
        related_name="completions",
        help_text="Lesson that was completed."
    )

    class Meta:
        db_table = "lesson_completions"
        unique_together = ["enrollment", "lesson"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.enrollment.student.full_name} - {self.lesson.title}"