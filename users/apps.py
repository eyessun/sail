from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # 如果有信号需要注册，导入signals模块
        pass  # 本例中不需要，因为我们不使用信号