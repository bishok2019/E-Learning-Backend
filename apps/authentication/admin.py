from django.contrib import admin

# Register your models here.
from .models import CustomUser, CustomPermission, Roles, PermissionCategory
admin.site.register([CustomUser,CustomPermission,Roles,PermissionCategory])
# admin.site.register(CustomPermission)
# admin.site.register(Roles)
# admin.site.register(PermissionCategory)