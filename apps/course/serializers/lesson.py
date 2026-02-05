from django.db import transaction
from rest_framework import serializers

from base.serializers import BaseModelSerializer

from ..models import Lesson


class LessonListSerializer(BaseModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "content",
            "order",
            "created_at",
            "created_by",
        ]


class BulkLessonCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "order",
            "content",
        ]

        read_only_fields = ["id"]


class LessonCreateSerializer(BaseModelSerializer):
    lesson = BulkLessonCreateSerializer(many=True)

    class Meta:
        model = Lesson
        fields = [
            "lesson",
            "course",
        ]
        # read_only_fields = ["id"]

    def validate(self, data):
        course = data.get("course")
        request = self.context.get("request")

        if course.instructor != request.user:
            raise serializers.ValidationError(
                {"course": ["You can only add lessons to your own courses."]}
            )

        # Check for duplicate order, valid for sinlgle lesson creation
        # order = data.get("order")
        # if Lesson.objects.filter(course=course, order=order).exists():
        #     raise serializers.ValidationError(
        #         {"order": "A lesson with this order already exists in the course."}
        #     )

        lessons = data.get("lesson", [])
        orders = [lesson["order"] for lesson in lessons]
        if len(orders) != len(set(orders)):
            raise serializers.ValidationError(
                {
                    "lessons": [
                        "Duplicate lesson order values in the request.",
                        lessons,
                    ],
                    "orders": [orders],
                }
            )
        # Check for existing orders in the DB

        existing_orders = set(
            Lesson.objects.filter(course=course, order__in=orders).values_list(
                "order", flat=True
            )
        )
        if existing_orders:
            raise serializers.ValidationError(
                {
                    "order": [
                        f"Lessons with these order values already exist in the course: {list(existing_orders)}"
                    ]
                }
            )
        return data

    @transaction.atomic
    def create(self, validated_data):
        lessons_data = validated_data.pop("lesson")
        course_details = validated_data.get("course")

        created_lesson = [
            Lesson(
                course=course_details,
                title=lesson["title"],
                order=lesson["order"],
                content=lesson["content"],
            )
            for lesson in lessons_data
        ]
        Lesson.objects.bulk_create(created_lesson)
        return created_lesson

    def to_representation(self, instance):
        """Return the created lessons."""
        return {
            "message": "Lessons created successfully",
            "count": len(instance),
            "lessons": BulkLessonCreateSerializer(instance, many=True).data,
        }


# class LessonCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = [
#             "id",
#             "course",
#             "title",
#             "content",
#             "order",
#         ]
#         read_only_fields = ["id"]

#     def validate(self, data):
#         course = data.get("course")
#         request = self.context.get("request")

#         if course.instructor != request.user:
#             raise serializers.ValidationError(
#                 {"course": "You can only add lessons to your own courses."}
#             )

#         # Check for duplicate order
#         order = data.get("order")
#         if Lesson.objects.filter(course=course, order=order).exists():
#             raise serializers.ValidationError(
#                 {"order": "A lesson with this order already exists in the course."}
#             )

#         return data


class LessonUpdateSerializer(BaseModelSerializer):
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


class LessonDetailSerializer(BaseModelSerializer):
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
