import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


LOGGING = {
    "version": 1,

    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": (
                "{levelname} {asctime} "
                "{module} {message}"
            ),
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },

        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(
                BASE_DIR,
                "logs",
                "django.log",
            ),
            "formatter": "verbose",
        },
    },

    "loggers": {
        "django": {
            "handlers": [
                "console",
                "file",
            ],
            "level": "INFO",
            "propagate": True,
        },
    },
}