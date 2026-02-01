from django.utils import timezone
from rest_framework import serializers

from base.serializers import BaseModelSerializer

from ..models import CourseStatusEnum, Enrollment


class EnrollmentListSerializer(BaseModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    total_lessons = serializers.IntegerField(read_only=True)
    completed_lessons_count = serializers.IntegerField(read_only=True)
    completion_percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "student_name",
            "course",
            "course_title",
            "is_completed",
            "completed_at",
            "total_lessons",
            "completed_lessons_count",
            "completion_percentage",
            "created_at",
        ]


class EnrollmentCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            "id",
            "course",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        request = self.context.get("request")
        course = data.get("course")
        student = request.user

        # handling enrollment to unpublished courses
        if course.status != CourseStatusEnum.PUBLISHED:
            raise serializers.ValidationError(
                {"course": "You can only enroll in published courses."}
            )
        {"course": "Instructors cannot enroll in their own courses."}

        # handling duplicate enrollment
        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError(
                {"course": "You are already enrolled in this course."}
            )

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["student"] = request.user
        return super().create(validated_data)


class EnrollmentDetailSerializer(BaseModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    total_lessons = serializers.IntegerField(read_only=True)
    completed_lessons_count = serializers.IntegerField(read_only=True)
    completion_percentage = serializers.FloatField(read_only=True)
    completed_lesson_ids = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "student_name",
            "course",
            "course_title",
            "is_completed",
            "completed_at",
            "total_lessons",
            "completed_lessons_count",
            "completion_percentage",
            "completed_lesson_ids",
            "created_at",
        ]

    def get_completed_lesson_ids(self, obj):
        return list(obj.completed_lessons.values_list("lesson_id", flat=True))
