from .dev import *  # noqa

CMDB_USE_SAMPLE_DATA = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
MIDDLEWARE = tuple(
    item for item in MIDDLEWARE if not item.startswith("blueapps.account.middlewares.")
)
