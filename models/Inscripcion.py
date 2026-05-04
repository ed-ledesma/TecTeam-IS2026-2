class Inscripcion(db.Model):
    __tablename__ = "inscripcion"

    id_alumno = db.Column(
        db.Integer,
        db.ForeignKey("alumno.id_usuario"),
        primary_key=True
    )

    id_curso = db.Column(
        db.Integer,
        db.ForeignKey("curso.id_curso"),
        primary_key=True
    )

    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)
    estado_inscripcion = db.Column(db.String(50))

    alumno = db.relationship("Alumno")
    curso = db.relationship("Curso")