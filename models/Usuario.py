from models import db

class Usuario(db.Model):
    __tablename__ = "usuario"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False)

    fecha_nacimiento = db.Column(db.Date, nullable=False)
    activo = db.Column(db.Boolean, default=True)

    password_hash = db.Column(db.String(255), nullable=False)

    ultimo_cambio_password = db.Column(db.DateTime)
    ultimo_acceso = db.Column(db.DateTime)