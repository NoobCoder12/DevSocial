from django.apps import AppConfig

app_name = 'users'


class UsersConfig(AppConfig):
    name = 'backend.apps.users'

    def ready(self):
        """
        Loads signals when all apps are ready
        """
        import backend.apps.users.signals