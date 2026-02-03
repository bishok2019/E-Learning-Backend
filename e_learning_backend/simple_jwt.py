from datetime import timedelta

from decouple import config

_SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ALGORITHM": config("TOKEN_ALGORITHM", default="HS256"),
    # "SIGNING_KEY": config("TOKEN_SIGNING_KEY", default="my_top_secret"),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    # "ALGORITHM": "HS256",
    "SIGNING_KEY": config("_SECRET_KEY", cast=str),
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
