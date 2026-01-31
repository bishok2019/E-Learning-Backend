from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value):
        try:
            token = RefreshToken(value)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError(
                {
                    "message": "User is already logged out or token is invalid.",
                    "detail": e,
                }
            )
        return value
