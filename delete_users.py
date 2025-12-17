from extensios import db
from main import app
from models import Users

with app.app_context():
    db.session.query(Users).delete()
    db.session.commit()