from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework import serializers

from ..models import Enrollment, Progress
from ..tasks import handle_course_completion


class LessonCompletionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = [
            "lesson",
        ]

    def validate(self, data):
        # Get enrollment from context (passed from view via URL)
        enrollment = self.context.get("enrollment")
        if not enrollment:
            raise serializers.ValidationError(
                {"enrollment": "Enrollment not found or does not belong to you."}
            )

        lesson = data.get("lesson")
        request = self.context.get("request")

        # Check if the lesson belongs to the enrolled course
        if lesson.course != enrollment.course:
            raise serializers.ValidationError(
                {"lesson": "This lesson does not belong to the enrolled course."}
            )

        # Check if already completed
        if Progress.objects.filter(enrollment=enrollment, lesson=lesson).exists():
            raise serializers.ValidationError(
                {"lesson": "You have already completed this lesson."}
            )

        # Check sequential order: ensure previous lessons are completed
        # Get all lessons for this course ordered by their order field
        all_lessons = list(
            lesson.course.lessons.filter(deleted_at__isnull=True)
            .order_by("order")
            .values_list("id", "order")
        )

        # Find current lesson's position
        current_lesson_index = next(
            (i for i, (lid, _) in enumerate(all_lessons) if lid == lesson.id), None
        )

        if current_lesson_index is None:
            raise serializers.ValidationError(
                {"lesson": "This lesson does not exist in the course."}
            )

        # Check if all previous lessons are completed
        if current_lesson_index > 0:
            previous_lesson_ids = [lid for lid, _ in all_lessons[:current_lesson_index]]
            completed_lesson_ids = Progress.objects.filter(
                enrollment=enrollment, lesson_id__in=previous_lesson_ids
            ).values_list("lesson_id", flat=True)

            if len(completed_lesson_ids) < len(previous_lesson_ids):
                uncompleted = [
                    lid
                    for lid in previous_lesson_ids
                    if lid not in completed_lesson_ids
                ]
                raise serializers.ValidationError(
                    {
                        "lesson": f"You must complete previous lessons first. Uncompleted lesson IDs: {uncompleted}"
                    }
                )

        # Store enrollment in validated data for create method
        data["enrollment"] = enrollment
        return data

    @transaction.atomic
    def create(self, validated_data):
        try:
            # concurrent completion update safety with locking enrollment row
            enrollment = Enrollment.objects.select_for_update().get(
                id=validated_data["enrollment"].id
            )
            lesson_completion = super().create(
                validated_data
            )  # create the Progress record

            # check if all lessons are completed then update enrollment status
            total_lessons = enrollment.total_lessons
            completed_lessons = enrollment.completed_lessons_count

            if total_lessons > 0 and completed_lessons >= total_lessons:
                enrollment.is_completed = True
                enrollment.completed_at = timezone.now()
                enrollment.save()

                # trigger background task
                transaction.on_commit(
                    lambda: handle_course_completion.delay(enrollment.id)
                )

            return lesson_completion

        except IntegrityError:
            # Handle race condition: lesson was completed by concurrent request
            # Database constraint prevented duplicate, return error gracefully
            raise serializers.ValidationError(
                {"lesson": "You have already completed this lesson."}
            )


class LessonCompletionListSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)

    class Meta:
        model = Progress
        fields = [
            "id",
            "enrollment",
            "lesson",
            "lesson_title",
            "created_at",
        ]
