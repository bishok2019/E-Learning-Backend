from django.db import transaction
from rest_framework import serializers


class ExcludeFieldsForMain:
    exclude = []  # We need all data in main


class ReadOnlyFields:
    read_only = [
        "created_by",
        "created_at",
        "updated_at",
        "modified_by",
        "deleted_at",
        "device_type",
        "os_type",
    ]


class ExcludeFields:
    exclude = [
        "created_by",
        "created_at",
        "updated_at",
        "modified_by",
        "deleted_at",
        "device_type",
        "os_type",
    ]


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", [])
        include_fields = kwargs.pop("include_fields", [])
        super().__init__(*args, **kwargs)
        for field_name in exclude_fields:
            self.fields.pop(field_name, None)

        # Include only specified fields
        if include_fields:
            new_fields = {
                field_name: self.fields[field_name] for field_name in include_fields
            }
            self.fields = new_fields

    @transaction.atomic
    def create(self, validated_data):
        request_data = self.context.get("request")
        validated_data.pop("id", None)
        if not request_data:
            raise serializers.ValidationError(
                {
                    "message": "Invalid request. `request` needs to be passed "
                    "while creating the data"
                }
            )
        try:
            user_id = self.context.get("request").user.id
        except Exception:
            raise serializers.ValidationError(
                {"message": "Invalid request. Invalid user."}
            )
        if user_id:
            validated_data["created_by"] = user_id
            validated_data["modified_by"] = user_id
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        request_data = self.context.get("request")
        if not request_data:
            raise serializers.ValidationError(
                {
                    "message": "Invalid request. `request` needs to be passed "
                    "while updating the data"
                }
            )

        try:
            user_id = self.context.get("request").user.id
        except Exception:
            raise serializers.ValidationError(
                {"message": "Invalid request. Invalid user."}
            )

        if not user_id:
            raise serializers.ValidationError(
                {
                    "message": "Failed to update the instance",
                    "detail": "Public user can not update the data",
                }
            )
        validated_data["modified_by"] = user_id
