from django.db import models
from base.models import AbstractBaseModel


class CourseStatusEnum(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"


class Course(AbstractBaseModel):
    title = models.CharField(
        max_length=255,
        help_text="Title of the course."
    )
    description = models.TextField(
        blank=True,
        help_text="Description of the course."
    )
    status = models.CharField(
        max_length=20,
        choices=CourseStatusEnum.choices,
        default=CourseStatusEnum.DRAFT,
        help_text="Publication status of the course."
    )
    instructor = models.ForeignKey(
        "authentication.CustomUser",
        on_delete=models.CASCADE,
        related_name="courses",
        help_text="Instructor who created the course."
    )

    class Meta:
        db_table = "courses"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.status == CourseStatusEnum.PUBLISHED

    @property
    def total_lessons(self):
        return self.lessons.count()