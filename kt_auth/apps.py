from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    auth_user_model = 'kt_auth.CustomUser'
    name = 'kt_auth'
    label = 'kt_auth'

