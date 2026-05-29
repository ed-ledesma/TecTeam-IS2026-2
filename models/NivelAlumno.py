from models import db

class NivelAlumno(db.Model):
    __tablename__ = "nivel_alumno"

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("alumno.id_usuario"),
        primary_key=True
    )

    id_idioma = db.Column(
        db.Integer,
        db.ForeignKey("idioma.id_idioma"),
        primary_key=True
    )

    nivel = db.Column(
        db.Integer,
        nullable=False
    )

    alumno = db.relationship("Alumno")
    idioma = db.relationship("Idioma")