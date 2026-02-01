from rest_framework import serializers

from ..models import CustomUser


class CustomUserSignUpSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    email_address = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            # "username",
            "password",
            "email_address",
        ]

    def validate(self, data):
        # username = data["username"]
        # if CustomUser.objects.filter(username__iexact=username).exists():
        #     raise serializers.ValidationError(
        #         {"username": "User already exists. Please sign in."}
        #     )

        email = data.get("email_address")
        if email and CustomUser.objects.filter(email_address__iexact=email).exists():
            raise serializers.ValidationError({"email_address": "Email already exists."})

        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        # validated_data["username"] = validated_data["username"].lower()

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()

        # UserProfile.objects.create(user=user)

        return user
