from rest_framework import serializers

from base.serializers import BaseModelSerializer

from ..models import CustomPermission, CustomUser, Roles


class CustomUserCreateSerializer(BaseModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Roles.objects.all(),
        required=False,
    )
    permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomPermission.objects.all(),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserUpdateSerializer(BaseModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Roles.objects.all(),
        required=False,
    )
    permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomPermission.objects.all(),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserRetrieveSerializer(BaseModelSerializer):
    roles = serializers.StringRelatedField(many=True)
    permissions = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        fields = "__all__"


class UserListSerializer(BaseModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            # "username",
            "email_address",
            "first_name",
            "last_name",
            "is_active",
            "created_at",
        ]


class ChangePasswordSerializer(BaseModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            "old_password",
            "password",
            "confirm_password",
        ]
        extra_kwargs = {
            "old_password": {"required": True},
            "password": {"required": True},
            "confirm_password": {"required": True},
        }

    def validate_password(self, password):
        if len(password) < 6:
            serializers.ValidationError("Password must be at least 6 characters")
        if len(password) > 32:
            serializers.ValidationError("Password must be max 32 characters")
        if str(password).isalpha():
            serializers.ValidationError(
                "Password must contain at least alphabets and numbers"
            )
        return password

    def validate(self, attrs):
        user = self.context["view"].kwargs.get("user")
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct."}
            )
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
