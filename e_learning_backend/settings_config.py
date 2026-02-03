from decouple import config

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")], default="*"
)

APPEND_SLASH = False


# CORS_ALLOWED_ORIGINS = config(
#     "CORS_ALLOWED_ORIGINS",
#     cast=lambda v: [s.strip() for s in v.split(",")],
#     default=f"http://localhost:{config('NGINX_EXPOSE_PORT')}, http://localhost:{config('BACKEND_EXPOSE_PORT')}",
# )

# CSRF_TRUSTED_ORIGINS = config(
#     "CSRF_TRUSTED_ORIGINS",
#     cast=lambda v: [s.strip() for s in v.split(",")],
#     default=f"http://localhost:{config('NGINX_EXPOSE_PORT')}, http://localhost:{config('BACKEND_EXPOSE_PORT')}",
# )

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default="http://localhost:8000",
)


DECIMAL_PLACES = config("DECIMAL_PLACES", cast=int, default=4)
MAX_DIGITS = config("MAX_DIGITS", cast=int, default=12)
MAX_DECIMAL_DIGITS = config("MAX_DECIMAL_DIGITS", cast=int, default=16)

## File and Image size for validators
FILE_MAX_UPLOAD_SIZE = config("FILE_MAX_UPLOAD_SIZE", cast=int, default=2) * 1024 * 1024
IMAGE_MAX_UPLOAD_SIZE = (
    config("IMAGE_MAX_UPLOAD_SIZE", cast=int, default=2) * 1024 * 1024
)

FILE_HELP_TEXT_SIZE = f"{config('FILE_MAX_UPLOAD_SIZE', cast=int, default=2)}"
IMAGE_HELP_TEXT_SIZE = f"{config('IMAGE_MAX_UPLOAD_SIZE', cast=int, default=2)}"
## File and Image size for validators


# Payload size memory usage config
MAX_UPLOAD_SIZE_MB = config(
    "MAX_UPLOAD_SIZE_MB", cast=int, default=30
)  # Allowed payload size

MAX_UPLOAD_FILE_SIZE_MB = config(
    "MAX_UPLOAD_FILE_SIZE_MB", cast=float, default=0.1
)  # 100KB by default
# Upto 100Kb the file will be stored in memory, For more than that, data
# will be uploaded in server temporarily which will be handled by FILE_UPLOAD_HANDLERS.


DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE_MB * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_FILE_SIZE_MB * 1024 * 1024
# This is to let the django upload data in memory, so that the request can proceed.
# Payload size memory usage config

MAX_UPLOAD_SIZE = DATA_UPLOAD_MAX_MEMORY_SIZE


# def copy_default_images():
#     """
#     We won't be editing media dir
#     media dir will reside in .gitignore
#     So, we are not doing any manual work
#     to copy media files,
#     and pushing to git repo.
#     """

#     # Default Images source that exist in the root
#     destination_for_source = BASE_DIR / "default_images"

#     # Path for the default images that will be copied into
#     destination_for_default_folder = MEDIA_ROOT / "default_images"
#     if not os.path.exists(destination_for_default_folder):
#         os.makedirs(destination_for_default_folder)

#     try:
#         shutil.copytree(
#             destination_for_source, destination_for_default_folder, dirs_exist_ok=True
#         )
#     except Exception as e:
#         pass
#     return None


# try:
#     copy_default_images()
# except Exception:
#     pass


INTERNAL_IPS = []
SERVER_ENV = config("SERVER_ENV", cast=bool, default=True)

DISABLED_AUTHENTICATION = config("DISABLED_AUTHENTICATION", cast=bool, default=False)
# TENANT_MODEL = "tenant.Tenant"
# TENANT_DOMAIN_MODEL = "customers.Domain" # app.Model
# DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)
# from django.templatetags.static import static
# from django.utils.translation import gettext_lazy as _

# UNFOLD = {
#     "SITE_TITLE": "iBiSAP",
#     "SITE_HEADER": "iBiSAP Backend Dashboard",
#     "SITE_SYMBOL": "speed",  # symbol from icon set
#     "SHOW_HISTORY": True,  # show/hide "History" button, default: True
#     "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
#     # "THEME": "dark",  # Force theme: "dark" or "light". Will disable theme switcher
#     "STYLES": [
#         lambda request: static("css/style.css"),
#     ],
#     "SCRIPTS": [
#         lambda request: static("js/script.js"),
#     ],
#     "COLORS": {
#         "font": {
#             "subtle-light": "107 114 128",
#             "subtle-dark": "156 163 175",
#             "default-light": "75 85 99",
#             "default-dark": "209 213 219",
#             "important-light": "17 24 39",
#             "important-dark": "243 244 246",
#         },
#         "primary": {
#             "50": "250 245 255",
#             "100": "243 232 255",
#             "200": "233 213 255",
#             "300": "216 180 254",
#             "400": "192 132 252",
#             "500": "168 85 247",
#             "600": "147 51 234",
#             "700": "126 34 206",
#             "800": "107 33 168",
#             "900": "88 28 135",
#             "950": "59 7 100",
#         },
#     },
#     "EXTENSIONS": {
#         "modeltranslation": {
#             "flags": {
#                 "en": "🇬🇧",
#                 "fr": "🇫🇷",
#                 "nl": "🇧🇪",
#             },
#         },
#     },
#     "SIDEBAR": {
#         "show_search": True,  # Search in applications and models names
#         "show_all_applications": False,  # Dropdown with all applications and models
#     },
# }

SECURE_PROXY = config("SECURE_PROXY", cast=bool, default=False)
if SECURE_PROXY:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# from django.templatetags.static import static
# from django.utils.translation import gettext_lazy as _

# UNFOLD = {
#     "SITE_TITLE": "iBiSAP",
#     "SITE_HEADER": "iBiSAP Backend Dashboard",
#     "SITE_SYMBOL": "speed",  # symbol from icon set
#     "SHOW_HISTORY": True,  # show/hide "History" button, default: True
#     "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
#     # "THEME": "dark",  # Force theme: "dark" or "light". Will disable theme switcher
#     "STYLES": [
#         lambda request: static("css/style.css"),
#     ],
#     "SCRIPTS": [
#         lambda request: static("js/script.js"),
#     ],
#     "COLORS": {
#         "font": {
#             "subtle-light": "107 114 128",
#             "subtle-dark": "156 163 175",
#             "default-light": "75 85 99",
#             "default-dark": "209 213 219",
#             "important-light": "17 24 39",
#             "important-dark": "243 244 246",
#         },
#         "primary": {
#             "50": "250 245 255",
#             "100": "243 232 255",
#             "200": "233 213 255",
#             "300": "216 180 254",
#             "400": "192 132 252",
#             "500": "168 85 247",
#             "600": "147 51 234",
#             "700": "126 34 206",
#             "800": "107 33 168",
#             "900": "88 28 135",
#             "950": "59 7 100",
#         },
#     },
#     "EXTENSIONS": {
#         "modeltranslation": {
#             "flags": {
#                 "en": "🇬🇧",
#                 "fr": "🇫🇷",
#                 "nl": "🇧🇪",
#             },
#         },
#     },
#     "SIDEBAR": {
#         "show_search": True,  # Search in applications and models names
#         "show_all_applications": False,  # Dropdown with all applications and models
#     },
# }


# from django.templatetags.static import static
# from django.utils.translation import gettext_lazy as _

# UNFOLD = {
#     "SITE_TITLE": "iBiSAP",
#     "SITE_HEADER": "iBiSAP Backend Dashboard",
#     "SITE_SYMBOL": "speed",  # symbol from icon set
#     "SHOW_HISTORY": True,  # show/hide "History" button, default: True
#     "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
#     # "THEME": "dark",  # Force theme: "dark" or "light". Will disable theme switcher
#     "STYLES": [
#         lambda request: static("css/style.css"),
#     ],
#     "SCRIPTS": [
#         lambda request: static("js/script.js"),
#     ],
#     "COLORS": {
#         "font": {
#             "subtle-light": "107 114 128",
#             "subtle-dark": "156 163 175",
#             "default-light": "75 85 99",
#             "default-dark": "209 213 219",
#             "important-light": "17 24 39",
#             "important-dark": "243 244 246",
#         },
#         "primary": {
#             "50": "250 245 255",
#             "100": "243 232 255",
#             "200": "233 213 255",
#             "300": "216 180 254",
#             "400": "192 132 252",
#             "500": "168 85 247",
#             "600": "147 51 234",
#             "700": "126 34 206",
#             "800": "107 33 168",
#             "900": "88 28 135",
#             "950": "59 7 100",
#         },
#     },
#     "EXTENSIONS": {
#         "modeltranslation": {
#             "flags": {
#                 "en": "🇬🇧",
#                 "fr": "🇫🇷",
#                 "nl": "🇧🇪",
#             },
#         },
#     },
#     "SIDEBAR": {
#         "show_search": True,  # Search in applications and models names
#         "show_all_applications": False,  # Dropdown with all applications and models
#     },
# }
