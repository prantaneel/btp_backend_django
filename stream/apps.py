from django.apps import AppConfig

class StreamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stream'
    def ready(self):
        from . import signals
        from .mqtt_consumer import client
        client.loop_start()
        
        