from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Client(db.Model, SerializerMixin):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    message = db.Column(db.String)

    def __repr__(self):
        return f"name= {self.name} , email = {self.email}"