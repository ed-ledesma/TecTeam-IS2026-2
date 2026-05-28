from tests.factories import crear_curso, crear_idioma, crear_profesor, iniciar_sesion
from utils.auth import ROL_PROFESOR


def test_profesor_publica_curso_propio(client):
    idioma = crear_idioma()
    profesor = crear_profesor()
    curso = crear_curso(profesor, idioma, estado="borrador")
    iniciar_sesion(client, profesor, ROL_PROFESOR)

    respuesta = client.post(f"/profesor/cursos/{curso.id_curso}/publicar")

    assert respuesta.status_code == 302
    assert curso.estado_curso == "publicado"


def test_profesor_no_publica_curso_de_otro_profesor(client):
    idioma = crear_idioma()
    profesor_dueno = crear_profesor(correo="dueno@sgci.test", numero_empleado="EMP-100")
    profesor_intruso = crear_profesor(correo="intruso@sgci.test", numero_empleado="EMP-101")
    curso = crear_curso(profesor_dueno, idioma, estado="borrador")
    iniciar_sesion(client, profesor_intruso, ROL_PROFESOR)

    respuesta = client.post(f"/profesor/cursos/{curso.id_curso}/publicar")

    assert respuesta.status_code == 403
    assert curso.estado_curso == "borrador"
