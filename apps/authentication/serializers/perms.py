from apps.authentication.models.perms import CustomPermission, PermissionCategory, Roles
from apps.authentication.utils import PermissionLists
from base.serializers import BaseModelSerializer, ExcludeFields, serializers


class PermissionSerializer(BaseModelSerializer):
    class Meta:
        model = CustomPermission
        fields = [
            "id",
            "name",
            "code_name",
        ]


class PermissionDropdownSerializer(BaseModelSerializer):
    class Meta:
        model = CustomPermission
        fields = [
            "id",
            "name",
        ]


class PermissionCategorySerializer(BaseModelSerializer):
    class Meta:
        model = PermissionCategory
        exclude = ExcludeFields.exclude


class RolesSerializer(BaseModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Roles
        exclude = ExcludeFields.exclude


class RolesListSerializer(BaseModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Roles
        exclude = ExcludeFields.exclude


class RolesCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Roles
        exclude = ExcludeFields.exclude

    def validate(self, attrs):
        role_name = attrs.get("name")
        if role_name == PermissionLists.SUPPORT_ROLE_NAME:
            raise serializers.ValidationError(
                {"name": f"Role with name '{role_name}' cannot be create or updated"}
            )
        return super().validate(attrs)


class RolesUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Roles
        exclude = ExcludeFields.exclude

    def validate(self, attrs):
        role_name = attrs.get("name")
        if role_name == PermissionLists.SUPPORT_ROLE_NAME:
            raise serializers.ValidationError(
                {"name": f"Role with name '{role_name}' cannot be create or updated"}
            )
        return super().validate(attrs)


class RolesRetrieveSerializer(BaseModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Roles
        exclude = ExcludeFields.exclude


class RolesListSerializerDropdown(BaseModelSerializer):
    class Meta:
        model = Roles
        fields = ["id", "name", "is_active"]
