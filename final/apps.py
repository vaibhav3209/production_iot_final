from django.apps import AppConfig

# register evrey time you create a new app
class FinalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'final'
