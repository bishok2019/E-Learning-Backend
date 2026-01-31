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
