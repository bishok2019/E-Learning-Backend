from django.db import models
from base.models import AbstractBaseModel


class Lesson(AbstractBaseModel):
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="lessons",
        help_text="Course this lesson belongs to."
    )
    title = models.CharField(
        max_length=255,
        help_text="Title of the lesson."
    )
    content = models.TextField(
        blank=True,
        help_text="Content of the lesson (plain text)."
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order index of the lesson within the course."
    )

    class Meta:
        db_table = "lessons"
        ordering = ["order", "created_at"]
        unique_together = ["course", "order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"