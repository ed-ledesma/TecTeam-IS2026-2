class Alumno(db.Model):
    __tablename__ = "alumno"

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id_usuario"),
        primary_key=True
    )

    matricula = db.Column(db.String(50), unique=True, nullable=False)

    usuario = db.relationship("Usuario")