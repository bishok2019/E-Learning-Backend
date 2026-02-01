from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.managers import CustomUserManager
from base.models import AbstractBaseModel, models


def upload_path_user(instance, filename):
    return "/".join(["user_image", filename])


def validate_image(image):
    file_size = image.size
    limit_byte_size = settings.MAX_UPLOAD_SIZE
    if file_size > limit_byte_size:
        # converting into kb
        f = limit_byte_size / 1024
        # converting into MB
        f = f / 1024
        raise ValidationError("Max size of file is %s MB" % f)


class UserTypeEnum(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    STUDENT = "STUDENT", "Student"
    INSTRUCTOR = "INSTRUCTOR", "Instructor"


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    user_type = models.CharField(
        max_length=20,
        choices=UserTypeEnum.choices,
        default=UserTypeEnum.STUDENT,
        help_text="Enum field for the user type.",
    )
    first_name = models.CharField(
        max_length=50,
        blank=True,
        help_text="First name can have max_length upto 50 characters, blank=True",
    )
    middle_name = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Middle name can have max_length upto 50 characters, blank=True",
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        help_text="Last name can have max_length upto 50 characters, blank=True",
    )

    full_name = models.CharField(
        max_length=255, blank=True, null=True, help_text="Full name of the user."
    )
    email_address = models.EmailField(
        max_length=255, unique=True, help_text="Email address of the user."
    )

    roles = models.ManyToManyField("authentication.Roles", blank=True)
    permissions = models.ManyToManyField("authentication.CustomPermission", blank=True)

    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active.",
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    profile_image = models.ImageField(
        upload_to=upload_path_user,
        blank=True,
        null=True,
        validators=[validate_image],
        help_text="Profile image of the user.",
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text="Designates that this user has all permissions without explicitly assigning them.",
    )
    is_blocked = models.BooleanField(
        default=False,
        help_text="Designates whether this user account is blocked.",
    )
    objects = CustomUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email_address"

    @property
    def get_permissions(self):
        return [_.code_name for _ in self.permissions.all()]

    @property
    def get_roles(self):
        return [_.name for _ in self.roles.all()]

    @property
    def get_all_permissions(self):
        return {
            "permissions": self.get_permissions,
            "roles": self.get_roles,
        }

    def tokens(self, request):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            # "username": self.username,
            "email_address": self.email_address,
            "full_name": self.full_name,
            "is_superuser": self.is_superuser,
            "id": self.id,
            "user_type": self.user_type,
            **self.get_all_permissions,
        }

    def save(self, *args, **kwargs):
        names = [self.first_name, self.middle_name, self.last_name]
        self.full_name = " ".join(name for name in names if name)
        super().save(*args, **kwargs)
