from models import db
from models.Profesor import Profesor
from models.Usuario import Usuario
from tests.factories import (
    crear_administrador,
    crear_profesor,
    datos_formulario_usuario,
    iniciar_sesion,
)
from utils.auth import ROL_ADMINISTRADOR, ROL_PROFESOR


def test_admin_actualiza_datos_de_profesor(client):
    admin = crear_administrador()
    profesor_usuario = crear_profesor(correo="profesor.editar@sgci.test", numero_empleado="EMP-400")
    iniciar_sesion(client, admin, ROL_ADMINISTRADOR)

    respuesta = client.post(
        f"/admin/usuarios/{profesor_usuario.id_usuario}/editar",
        data=datos_formulario_usuario(
            nombres="Profesor Actualizado",
            apellido_paterno="Nuevo",
            apellido_materno="Nombre",
            correo="profesor.actualizado@sgci.test",
            fecha_nacimiento="1989-02-10",
            password="",
            rol=ROL_PROFESOR,
            matricula="",
            numero_empleado="EMP-401",
            especialidad="Italiano",
            fecha_contratacion="2024-04-01",
        ),
    )

    usuario = db.session.get(Usuario, profesor_usuario.id_usuario)
    profesor = db.session.get(Profesor, profesor_usuario.id_usuario)

    assert respuesta.status_code == 302
    assert usuario.correo == "profesor.actualizado@sgci.test"
    assert usuario.nombres == "Profesor Actualizado"
    assert profesor.numero_empleado == "EMP-401"
    assert profesor.especialidad == "Italiano"
