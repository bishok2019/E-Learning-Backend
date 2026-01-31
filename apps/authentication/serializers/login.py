from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        username = attrs.get("username", "").lower()
        password = attrs.get("password")

        if not username:
            raise serializers.ValidationError(
                {
                    "username": "Email or Username is required.",
                }
            )

        user = User.objects.filter(
            Q(email__iexact=username) | Q(username__iexact=username)
        ).first()

        if not user:
            raise serializers.ValidationError({"username": "User not found."})

        user = authenticate(request=request, username=user.username, password=password)

        if not user:
            raise serializers.ValidationError({"password": "Invalid credentials."})

        if not user.is_active:
            raise serializers.ValidationError({"username": "User is not active."})

        if user.is_blocked:
            raise serializers.ValidationError({"username": "Account is blocked."})

        data = user.tokens(request)
        return data
