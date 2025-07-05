from django.apps import AppConfig



class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    
    def ready(self):
        # Import signals to ensure they are registered
        import tasks.signals
