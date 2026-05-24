from models import db

class Profesor(db.Model):
    __tablename__ = "profesor"

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id_usuario"),
        primary_key=True
    )

    numero_empleado = db.Column(db.String(50), unique=True, nullable=False)
    especialidad = db.Column(db.String(100))
    fecha_contratacion = db.Column(db.Date, nullable=False)

    usuario = db.relationship("Usuario")