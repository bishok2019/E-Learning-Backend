_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",  # or 'DEBUG'
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        # Add your app logger if needed
        "apps.contents.views.content": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
