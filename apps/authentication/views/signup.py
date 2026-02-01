from rest_framework import generics, status
from rest_framework.response import Response

from ..serializers import CustomUserSignUpSerializer


class CustomUserSignUpAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSignUpSerializer
    permission_classes = []

    def post(self, request):
        serializer = CustomUserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # if 'role' not in request.data:
            #     default_role = Role.objects.get(name='Staff')
            #     user.role = default_role
            #     user.save()
            return Response(
                {
                    "status": "success",
                    "message": "User created successfully.",
                    "data": CustomUserSignUpSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
