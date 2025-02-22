from django.apps import AppConfig


class SphereConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sphere'
    def ready(self):
        import sphere.signals  # noqa: F401