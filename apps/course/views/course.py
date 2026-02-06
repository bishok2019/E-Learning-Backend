from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from apps.authentication.models import UserTypeEnum
from apps.authentication.perms.custom_perms import (
    CustomAuthenticationPermission,
    IsCourseCreator,
    IsEnrolled,
    IsInstructor,
    IsInstructorCreator,
)
from apps.authentication.utils import PermissionLists
from base.views.generic_views import (
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from ..models import Course, CourseStatusEnum
from ..serializers import (
    CourseCreateSerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    CourseUpdateSerializer,
)


class CourseListView(CustomGenericListView):
    """
    List all published courses for students.
    Instructors see all their own courses.
    """

    serializer_class = CourseListSerializer
    permission_classes = []
    # permission_classes = [IsInstructorCreator]
    queryset = Course.objects.all()

    # def get_queryset(self):
    #     user = self.request.user
    #     # if user.user_type == UserTypeEnum.INSTRUCTOR:
    #     # Instructors see their own courses
    #     # return Course.objects.filter(instructor=user)

    #     if user.user_type == UserTypeEnum.ADMIN:
    #         return Course.objects.all()  # Admins see all courses
    #         # Other see only published courses
    #     else:
    #         return Course.objects.filter(status=CourseStatusEnum.PUBLISHED)

    # def get_permissions(self):
    #     print("Getting permissions for CourseListView")
    #     return [
    #         CustomAuthenticationPermission(
    #             models={
    #                 PermissionLists.HTTP_POST_METHOD: PermissionLists.COURSE,
    #             },
    #         ),
    #         IsInstructor(),
    #         print("Permissions for CourseListView"),
    #     ]


class CourseCreateView(CustomGenericCreateView):
    """
    Create a new course (Instructors only).
    """

    serializer_class = CourseCreateSerializer
    permission_classes = []

    def get_permissions(self):
        return [
            CustomAuthenticationPermission(
                models={
                    PermissionLists.HTTP_POST_METHOD: PermissionLists.COURSE,
                },
            )
        ]


class CourseRetrieveView(CustomGenericRetrieveView):
    """
    Retrieve course details.
    """

    serializer_class = CourseDetailSerializer
    permission_classes = [IsEnrolled | IsInstructor]
    queryset = Course.objects.all()

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.user_type == UserTypeEnum.INSTRUCTOR:
    #         return Course.objects.filter(instructor=user)
    #     else:
    #         return Course.objects.filter(status=CourseStatusEnum.PUBLISHED)


class CourseUpdateView(CustomGenericUpdateView):
    """
    Update a course (Instructor owner only).
    """

    serializer_class = CourseUpdateSerializer
    permission_classes = [IsAuthenticated, IsInstructorCreator]

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)

    def get_permissions(self):
        return [
            CustomAuthenticationPermission(
                models={
                    PermissionLists.HTTP_PATCH_METHOD: PermissionLists.COURSE,
                },
            )
        ]


# class CourseDeleteView(CustomGenericUpdateView):
#     """
#     Delete a course (Instructor owner only).
#     """
#     permission_classes = [permissions.IsAuthenticated, IsInstructor, IsInstructorOwner]

#     def get_queryset(self):
#         return Course.objects.filter(instructor=self.request.user)
