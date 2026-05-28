from tests.factories import crear_administrador, crear_alumno, crear_profesor, iniciar_sesion
from utils.auth import ROL_ADMINISTRADOR, ROL_ALUMNO


def test_admin_consulta_lista_de_profesores(client):
    admin = crear_administrador()
    crear_profesor(correo="consulta.profesor@sgci.test", numero_empleado="EMP-333")
    iniciar_sesion(client, admin, ROL_ADMINISTRADOR)

    respuesta = client.get("/admin/profesores")

    assert respuesta.status_code == 200
    assert b"consulta.profesor@sgci.test" in respuesta.data
    assert b"EMP-333" in respuesta.data


def test_alumno_no_consulta_lista_de_profesores_de_admin(client):
    alumno = crear_alumno(correo="alumno.sin.admin@sgci.test")
    iniciar_sesion(client, alumno, ROL_ALUMNO)

    respuesta = client.get("/admin/profesores")

    assert respuesta.status_code == 403
