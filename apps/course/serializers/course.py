from rest_framework import serializers
from ..models import Course, CourseStatusEnum
from base.serializers import BaseModelSerializer, ExcludeFields
from .lesson import LessonListSerializer

class CourseListSerializer(BaseModelSerializer):
    instructor_name = serializers.CharField(source="instructor.full_name", read_only=True)
    total_lessons = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        # fields = [
        #     "id",
        #     "title",
        #     "short_description",
        #     "status",
        #     "instructor",
        #     "instructor_name",
        #     "total_lessons",
        #     "created_at",
        #     "updated_at",
        # ]
        exclude = ExcludeFields.exclude


class CourseCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Course
        fields = [
            "title",
            "description",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["instructor"] = request.user
        validated_data["status"] = CourseStatusEnum.DRAFT
        return super().create(validated_data)


class CourseUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Course
        fields = [
            "title",
            "description",
            "status",
        ]


class CourseDetailSerializer(BaseModelSerializer):
    instructor_name = serializers.CharField(source="instructor.full_name", read_only=True)
    total_lessons = serializers.IntegerField(read_only=True)
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "status",
            "instructor",
            "instructor_name",
            "total_lessons",
            "lessons",
            "created_at",
            "updated_at",
        ]

    def get_lessons(self, obj):
        lessons = obj.lessons.all().order_by("order")
        return LessonListSerializer(lessons, many=True).data