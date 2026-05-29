from models import db
from models.Usuario import Usuario
from tests.factories import crear_administrador, crear_alumno, iniciar_sesion
from utils.auth import ROL_ADMINISTRADOR


def test_admin_desactiva_cuenta_de_usuario(client):
    admin = crear_administrador()
    alumno = crear_alumno(correo="cuenta.eliminar@sgci.test", matricula="ALU-500")
    iniciar_sesion(client, admin, ROL_ADMINISTRADOR)

    respuesta = client.post(f"/admin/usuarios/{alumno.id_usuario}/desactivar")

    usuario = db.session.get(Usuario, alumno.id_usuario)
    assert respuesta.status_code == 302
    assert usuario.activo is False


def test_admin_reactiva_cuenta_de_usuario(client):
    admin = crear_administrador()
    alumno = crear_alumno(correo="cuenta.reactivar@sgci.test", activo=False, matricula="ALU-501")
    iniciar_sesion(client, admin, ROL_ADMINISTRADOR)

    respuesta = client.post(f"/admin/usuarios/{alumno.id_usuario}/activar")

    usuario = db.session.get(Usuario, alumno.id_usuario)
    assert respuesta.status_code == 302
    assert usuario.activo is True
