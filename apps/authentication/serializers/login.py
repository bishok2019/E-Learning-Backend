from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email_address = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        email = attrs.get("email_address", "").lower()
        password = attrs.get("password")

        if not email:
            raise serializers.ValidationError(
                {
                    "email_address": "Email is required.",
                }
            )

        user = User.objects.filter(
            Q(email_address__iexact=email)).first()

        if not user:
            raise serializers.ValidationError({"email_address": "User not found."})
        user = authenticate(request=request, email_address=user.email_address, password=password)

        if not user:
            raise serializers.ValidationError({"password": "Invalid credentials."})

        if not user.is_active:
            raise serializers.ValidationError({"email_address": "User is not active."})

        if user.is_blocked:
            raise serializers.ValidationError({"email_address": "Account is blocked."})

        data = user.tokens(request)
        return data
