class Administrador(db.Model):
    __tablename__ = "administrador"

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id_usuario"),
        primary_key=True
    )

    nivel_acceso = db.Integer, nullable=False
    area_responsable = db.Column(db.String(100))

    usuario = db.relationship("Usuario")