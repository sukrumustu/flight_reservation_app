from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    def ready(self) ->None:   # bu functionı oluşturduğumuz signali(user oluşturma sinyalini çalıştırmak için kullanıyoruz)
        import users.signals
