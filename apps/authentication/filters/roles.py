from django_filters import rest_framework as filters

from apps.authentication.models.perms import Roles


class RolesFilter(filters.FilterSet):
    date_range = filters.DateFromToRangeFilter(
        field_name="created_at",
        label="Created Between (start and end date)",
    )

    class Meta:
        model = Roles
        fields = ["date_range", "is_active"]
