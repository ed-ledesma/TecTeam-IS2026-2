from models import db

class Curso(db.Model):
    __tablename__ = "curso"

    id_curso = db.Column(db.Integer, primary_key=True)

    id_profesor = db.Column(
        db.Integer,
        db.ForeignKey("profesor.id_usuario"),
        nullable=False
    )

    id_idioma = db.Column(
        db.Integer,
        db.ForeignKey("idioma.id_idioma"),
        nullable=False
    )

    codigo = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    nivel_requerido = db.Column(
        db.Integer,
        nullable=False
    )

    modalidad = db.Column(db.String(50))

    cupo_maximo = db.Column(db.Integer)

    estado_curso = db.Column(db.String(50))

    profesor = db.relationship("Profesor")

    idioma = db.relationship("Idioma")