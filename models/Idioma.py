from models import db

class Idioma(db.Model):
    __tablename__ = "idioma"

    id_idioma = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )