from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.authentication.models.perms import CustomPermission, PermissionCategory, Roles
from apps.authentication.perms.perms_list import ALL_PERMISSION_LIST
from apps.authentication.utils import HttpBasedPermissionActionMaps, PermissionLists


class Command(BaseCommand):
    help = "Create custom permissions and categories dynamically."

    PERMISSION_TYPES = [
        HttpBasedPermissionActionMaps.CAN_CREATE,
        HttpBasedPermissionActionMaps.CAN_VIEW,
        HttpBasedPermissionActionMaps.CAN_UPDATE,
        HttpBasedPermissionActionMaps.CAN_DELETE,
    ]

    def create_perms(self):
        """
        Create only required permissions dynamically from ALL_PERMISSION_LIST.
        Code names will follow a consistent format: can_<action>_<model>.
        """
        # Fetch existing permissions
        existing_permissions_map = set(
            CustomPermission.objects.values_list("code_name", flat=True)
        )

        # Fetch existing categories
        existing_categories = {
            cat.name: cat for cat in PermissionCategory.objects.all()
        }

        self.stdout.write(self.style.WARNING("Preparing Permission & Categories"))

        # Collect unique category names from ALL_PERMISSION_LIST
        all_category_names = set()
        for app_name, models in ALL_PERMISSION_LIST.items():
            for model_name in models.keys():
                category_name = model_name.replace("_", " ").title()
                all_category_names.add(category_name)

        # Create missing categories if any
        new_categories = [
            PermissionCategory(name=category_name)
            for category_name in all_category_names
            if category_name not in existing_categories
        ]

        if new_categories:
            PermissionCategory.objects.bulk_create(new_categories)

            # Refresh existing categories after bulk insert
            existing_categories.update(
                {cat.name: cat for cat in PermissionCategory.objects.all()}
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Total '{len(new_categories)}' Permission Categories Created"
                )
            )

        self.stdout.write(self.style.WARNING("Preparing Custom Permissions"))

        to_bulk_create_permissions = []

        # Create permissions based on ALL_PERMISSION_LIST
        for app_name, models in ALL_PERMISSION_LIST.items():
            for model_name, actions in models.items():
                category_name = model_name.replace("_", " ").title()
                category = existing_categories.get(category_name)

                for action in actions:
                    code_name = f"can_{action}_{model_name}"
                    if code_name not in existing_permissions_map:
                        # Create readable name: e.g. "Can Create Content"
                        readable_name = f"Can {action.title()} {model_name.replace('_', ' ').title()}"
                        to_bulk_create_permissions.append(
                            CustomPermission(
                                name=readable_name,
                                code_name=code_name,
                                category=category,
                            )
                        )

        # Bulk create all new permissions at once
        if to_bulk_create_permissions:
            CustomPermission.objects.bulk_create(to_bulk_create_permissions)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Total '{len(to_bulk_create_permissions)}' Permissions Created"
                )
            )

    # def create_perms(self):
    #     existing_permissions_map = set(
    #         CustomPermission.objects.values_list("code_name", flat=True)
    #     )

    #     existing_categories = {
    #         cat.name: cat for cat in PermissionCategory.objects.all()
    #     }

    #     self.stdout.write(self.style.WARNING("Preparing Permission & Categories"))

    #     new_categories = [
    #         PermissionCategory(name=category_name.replace("_", " "))
    #         for category_name in PermissionLists.ALL_MODELS_LIST.keys()
    #         if category_name.replace("_", " ") not in existing_categories
    #     ]

    #     if new_categories:
    #         PermissionCategory.objects.bulk_create(new_categories)

    #         # refreshinh existing_categories with newly created ones
    #         existing_categories.update(
    #             {cat.name: cat for cat in PermissionCategory.objects.all()}
    #         )
    #         self.stdout.write(
    #             self.style.SUCCESS(
    #                 f"Total '{len(new_categories)}' Permissions Categories Created"
    #             )
    #         )
    #     self.stdout.write(self.style.WARNING("Preparing Custom Permission"))

    #     to_bulk_create_permissions = []

    #     for (
    #         category_name,
    #         model,
    #     ) in PermissionLists.ALL_MODELS_LIST.items():
    #         category = existing_categories.get(category_name.replace("_", " "))

    #         for perm_type in self.PERMISSION_TYPES:
    #             code_name = f"{perm_type}_{model}"
    #             if code_name not in existing_permissions_map:
    #                 to_bulk_create_permissions.append(
    #                     CustomPermission(
    #                         name=f"{perm_type.replace('_', ' ').title()} {model.replace('_', ' ').title()}",
    #                         code_name=code_name,
    #                         category=category,
    #                     )
    #                 )

    #     if to_bulk_create_permissions:
    #         CustomPermission.objects.bulk_create(to_bulk_create_permissions)
    #         self.stdout.write(
    #             self.style.SUCCESS(
    #                 f"Total '{len(to_bulk_create_permissions)}'Permissions created"
    #             )
    #         )

    def create_support_role(self):
        # ----------- creating support role with all permissoins
        all_existing_read_permissions = CustomPermission.objects.filter(
            code_name__startswith=HttpBasedPermissionActionMaps.CAN_VIEW
        )
        read_role, is_created = Roles.objects.get_or_create(
            name=PermissionLists.SUPPORT_ROLE_NAME,
            defaults={
                "remarks": "This Role is dedicated to VIEW Permissions Only",
                "is_active": True,
            },
        )
        read_role.permissions.set(all_existing_read_permissions)

    def assign_superuser_permissions(self):
        User = get_user_model()

        users = User.objects.filter(is_superuser=True)
        # users = User.objects.filter()
        user_roles = Roles.objects.all()
        user_permissions = CustomPermission.objects.all()
        for user in users:
            for role in user_roles:
                user.roles.add(role)
            for permission in user_permissions:
                user.permissions.add(permission)

    @transaction.atomic()
    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS("\nStarting permission and category creation...")
        )
        try:
            self.create_perms()
            self.create_support_role()
            self.assign_superuser_permissions()
            self.stdout.write(
                self.style.SUCCESS("\n Successfully created permission and category.")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during execution:{str(e)}"))

            raise
