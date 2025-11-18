# model/user_model.py

from model.database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(30), unique=True, nullable=False)

    chats = db.relationship("ChatHistory", backref="user", lazy=True)

    @staticmethod
    def get_or_create_user(phone_number):
        user = User.query.filter_by(phone_number=phone_number).first()
        if not user:
            user = User(phone_number=phone_number)
            db.session.add(user)
            db.session.commit()
        return user
