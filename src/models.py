from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=True)
    phone = db.Column(db.String, unique=False, nullable=True)

    def __repr__(self):
        return '<Contact %r>' % self.email

    def serialize(self):
        return {
            "full_name": self.full_name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone,
            "id": self.id

        }