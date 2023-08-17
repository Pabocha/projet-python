from django.apps import AppConfig


class InvestisseursConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'investisseurs'

    def ready(self):
        import investisseurs.signals
