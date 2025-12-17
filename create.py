from main import app
from extensios import db

with app.app_context():
    db.create_all()
    print('Таблицы успешно созданы!')