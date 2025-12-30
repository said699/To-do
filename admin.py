# Импорты
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, abort
from flask_admin import AdminIndexView

# класс, который наследуется от ModelView.Чтобы ограничить доступ к моделям в админке.
class AdminModelView(ModelView):
    # Flask-Admin сам вызывает этот метод, когда кто-то пытается зайти в админку.
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    # Этот метод вызывается, если is_accessible() вернул False.
    def inaccessible_callback(self, name, **kwargs):
        abort(404)

# Этот класс управляет главной страницей админки
class TodoAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        abort(404)