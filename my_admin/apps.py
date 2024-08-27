from django.apps import AppConfig


class AdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "my_admin"

    def ready(self):
        import my_admin.signals  # noqa: F401 or pylint: disable=unused-import
