from django.apps import AppConfig


class TurnoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'turno'
    def ready(self):
        import sys
        
        if 'runserver' in sys.argv:
            from turno.scheduler import iniciar_scheduler
            iniciar_scheduler()
   