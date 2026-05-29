from models.Profesor import Profesor
from models.Usuario import Usuario
from tests.factories import crear_administrador, datos_formulario_usuario, iniciar_sesion
from utils.auth import ROL_ADMINISTRADOR, ROL_PROFESOR


def test_admin_crea_profesor_desde_gestion_de_usuarios(client):
    admin = crear_administrador()
    iniciar_sesion(client, admin, ROL_ADMINISTRADOR)

    respuesta = client.post(
        "/admin/usuarios/crear",
        data=datos_formulario_usuario(
            nombres="Laura",
            apellido_paterno="García",
            apellido_materno="López",
            correo="laura.prof@sgci.test",
            rol=ROL_PROFESOR,
            matricula="",
            numero_empleado="EMP-777",
            especialidad="Alemán",
            fecha_contratacion="2025-01-10",
        ),
    )

    usuario = Usuario.query.filter_by(correo="laura.prof@sgci.test").one()
    profesor = Profesor.query.filter_by(id_usuario=usuario.id_usuario).one()

    assert respuesta.status_code == 302
    assert profesor.numero_empleado == "EMP-777"
    assert profesor.usuario.nombres == "Laura"
