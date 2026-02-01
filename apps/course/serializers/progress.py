from rest_framework import serializers
from django.utils import timezone
from ..models import Progress, Enrollment
from ..tasks import handle_course_completion
from django.db import transaction

class LessonCompletionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = [
            "enrollment",
            "lesson",
        ]

    def validate(self, data):
        enrollment = data.get("enrollment")
        lesson = data.get("lesson")
        request = self.context.get("request")

        # Check if the enrollment belongs to the current user
        if enrollment.student != request.user:
            raise serializers.ValidationError(
                {"enrollment": "You can only mark lessons complete for your own enrollments."}
            )

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

        return data
    
    @transaction.atomic
    def create(self, validated_data):
        # concurrent completion update safety with locking enrollment row
        enrollment = Enrollment.objects.select_for_update().get(
            id=validated_data["enrollment"].id
        )
        lesson_completion = super().create(validated_data) # create the Progress record
        
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