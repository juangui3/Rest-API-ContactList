from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    agenda_slug = db.Column(db.String(120), unique=False, nullable=False)
    address = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.full_name

    def serialize(self):
        return {
            "full_name": self.full_name,
            "email": self.email,
            "agenda_slug": self.agenda_slug,
            "address": self.address,
            "phone": self.phone,
            "id":self.id

        }