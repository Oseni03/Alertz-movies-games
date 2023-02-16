from django.apps import AppConfig


class AlertConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "alert"
    
    def ready(self):
        from jobs import updater 
        updater.start()