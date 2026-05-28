from models import db
from models.Usuario import Usuario
from tests.factories import crear_administrador, crear_profesor, iniciar_sesion
from utils.auth import ROL_ADMINISTRADOR


def test_admin_desactiva_profesor(client):
    admin = crear_administrador()
    profesor = crear_profesor(correo="profesor.eliminar@sgci.test", numero_empleado="EMP-500")
    iniciar_sesion(client, admin, ROL_ADMINISTRADOR)

    respuesta = client.post(f"/admin/usuarios/{profesor.id_usuario}/desactivar")

    usuario = db.session.get(Usuario, profesor.id_usuario)
    assert respuesta.status_code == 302
    assert usuario.activo is False


def test_profesor_desactivado_no_puede_iniciar_sesion(client):
    crear_profesor(correo="profesor.desactivado@sgci.test", password="Password123", activo=False)

    respuesta = client.post(
        "/login",
        data={"correo": "profesor.desactivado@sgci.test", "password": "Password123"},
    )

    assert respuesta.status_code == 403
