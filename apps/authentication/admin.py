from django.contrib import admin

# Register your models here.
from .models import CustomPermission, CustomUser, PermissionCategory, Roles

admin.site.register([CustomUser, CustomPermission, Roles, PermissionCategory])
# admin.site.register(CustomPermission)
# admin.site.register(Roles)
# admin.site.register(PermissionCategory)
