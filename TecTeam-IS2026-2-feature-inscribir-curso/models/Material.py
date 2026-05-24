from models import db
from datetime import datetime

class Material(db.Model):
    __tablename__ = "material"

    id_material = db.Column(db.Integer, primary_key=True)

    id_curso = db.Column(
        db.Integer,
        db.ForeignKey("curso.id_curso"),
        nullable=False
    )

    titulo = db.Column(db.String(150), nullable=False)
    tipo_material = db.Column(db.String(50))
    url_archivo = db.Column(db.String(255))

    visible = db.Column(db.Boolean, default=True)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)

    curso = db.relationship("Curso")