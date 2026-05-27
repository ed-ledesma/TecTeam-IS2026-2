from models.Alumno import Alumno
from models.Profesor import Profesor
from models.Usuario import Usuario
from tests.factories import (
    crear_administrador,
    datos_formulario_usuario,
    iniciar_sesion,
)
from utils.auth import ROL_ADMINISTRADOR, ROL_ALUMNO, ROL_PROFESOR


def test_admin_crea_cuenta_de_alumno(client):
    admin = crear_administrador()
    iniciar_sesion(client, admin, ROL_ADMINISTRADOR)

    respuesta = client.post(
        "/admin/usuarios/crear",
        data=datos_formulario_usuario(
            correo="nuevo.alumno@sgci.test",
            rol=ROL_ALUMNO,
            matricula="ALU-900",
        ),
    )

    usuario = Usuario.query.filter_by(correo="nuevo.alumno@sgci.test").one()
    alumno = Alumno.query.filter_by(id_usuario=usuario.id_usuario).one()

    assert respuesta.status_code == 302
    assert respuesta.location.endswith("/admin/usuarios")
    assert usuario.activo is True
    assert alumno.matricula == "ALU-900"


def test_admin_crea_cuenta_de_profesor(client):
    admin = crear_administrador()
    iniciar_sesion(client, admin, ROL_ADMINISTRADOR)

    respuesta = client.post(
        "/admin/usuarios/crear",
        data=datos_formulario_usuario(
            correo="nuevo.profesor@sgci.test",
            rol=ROL_PROFESOR,
            matricula="",
            numero_empleado="EMP-900",
            especialidad="Francés",
            fecha_contratacion="2024-08-01",
        ),
    )

    usuario = Usuario.query.filter_by(correo="nuevo.profesor@sgci.test").one()
    profesor = Profesor.query.filter_by(id_usuario=usuario.id_usuario).one()

    assert respuesta.status_code == 302
    assert profesor.numero_empleado == "EMP-900"
    assert profesor.especialidad == "Francés"
