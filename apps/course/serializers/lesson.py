from rest_framework import serializers

from ..models import Lesson


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "content",
            "order",
            "created_at",
        ]


class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "title",
            "content",
            "order",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        course = data.get("course")
        request = self.context.get("request")

        if course.instructor != request.user:
            raise serializers.ValidationError(
                {"course": "You can only add lessons to your own courses."}
            )

        # Check for duplicate order
        order = data.get("order")
        if Lesson.objects.filter(course=course, order=order).exists():
            raise serializers.ValidationError(
                {"order": "A lesson with this order already exists in the course."}
            )

        return data


class LessonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "title",
            "content",
            "order",
        ]

    def validate_order(self, value):
        instance = self.instance
        if (
            instance
            and Lesson.objects.filter(course=instance.course, order=value)
            .exclude(id=instance.id)
            .exists()
        ):
            raise serializers.ValidationError(
                "A lesson with this order already exists in the course."
            )
        return value


class LessonDetailSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "course_title",
            "title",
            "content",
            "order",
            "created_at",
        ]
