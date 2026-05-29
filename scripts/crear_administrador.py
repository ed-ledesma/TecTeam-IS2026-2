import os
from datetime import date, datetime

from werkzeug.security import generate_password_hash

from app import create_app
from models import db
from models.Administrador import Administrador
from models.Usuario import Usuario


def crear_administrador_inicial():
    correo = os.getenv("ADMIN_CORREO", "admin@sgci.com").strip().lower()
    password = os.getenv("ADMIN_PASSWORD", "Admin12345")

    usuario_existente = Usuario.query.filter_by(correo=correo).first()

    if usuario_existente is not None:
        print(f"Ya existe un usuario con el correo {correo}")
        return

    usuario = Usuario(
        nombres=os.getenv("ADMIN_NOMBRES", "Administrador"),
        apellido_paterno=os.getenv("ADMIN_APELLIDO_PATERNO", "General"),
        apellido_materno=os.getenv("ADMIN_APELLIDO_MATERNO", "Sistema"),
        correo=correo,
        fecha_nacimiento=date(1990, 1, 1),
        activo=True,
        password_hash=generate_password_hash(password),
        ultimo_cambio_password=datetime.utcnow(),
    )

    db.session.add(usuario)
    db.session.flush()

    administrador = Administrador(
        id_usuario=usuario.id_usuario,
        nivel_acceso=int(os.getenv("ADMIN_NIVEL_ACCESO", "1")),
        area_responsable=os.getenv("ADMIN_AREA_RESPONSABLE", "Sistema"),
    )

    db.session.add(administrador)
    db.session.commit()

    print(f"Administrador creado: {correo}")


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        crear_administrador_inicial()
